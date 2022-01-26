#!/usr/bin/env python
# -- coding: utf-8 --
import argparse
import logging
import os
import subprocess
import sys
import threading


from lib import conf_parser
from lib import starrocks_lib
from lib.config_util import ConfigUtil
from utility import logger


class StreamLoadThread(threading.Thread):
    def __init__(self, table_name, file_path):
        threading.Thread.__init__(self)
        self.table_name = table_name
        self.file_path = file_path
        self.lib = starrocks_lib.StarrocksLib()

    def run(self):
        logging.info("stream load start. table: %s, path: %s", self.table_name, self.file_path)
        cmd = self.lib.get_stream_load_cmd(self.file_path, self.table_name, ConfigUtil.get_columns(self.table_name))
        logging.info("stream load command: {%s}", cmd)
        res, output = subprocess.getstatusoutput(cmd)
        is_success = False
        msg = None
        error_url = None
        for line in output.split("\n"):
            if "\"Status\": \"Success\"" in line:
                is_success = True
            if "Message" in line:
                msg = line
            if "ErrorURL" in line:
                error_url = line

        if is_success:
            logging.info("stream load success. table: %s, path: %s", self.table_name, self.file_path)
        elif msg or error_url:
            logging.error("stream load error. table: %s, path: %s, msg: %s, error_url: %s",
                          self.table_name, self.file_path, msg, error_url)
        else:
            logging.error("unknown error. res: %s, output: {%s}", res, output)


class StarrocksDbTableOperation(object):
    def __init__(self):
        self.lib = starrocks_lib.StarrocksLib()

    def connect_starrocks(self):
        self.lib.connect()

    def close_starrocks(self):
        self.lib.close()

    def create_database(self, db_name):
        return self.lib.create_database(db_name)

    def use_database(self, db_name):
        self.lib.use_database(db_name)

    def create_db_table(self, data_dir_path):
        self.connect_starrocks()
        try:
            # create db
            starrocks_db = conf_parser.starrocks_db
            res = self.lib.create_database(starrocks_db)
            if res is None:
                print("create database error.")
                sys.exit(-1)
            if not res["status"]:
                print("create database error, msg: %s" % (res["msg"]))
                sys.exit(-1)

            # use db
            self.use_database(starrocks_db)

            # get create db table sql
            ddl_sqls = self.lib.get_create_db_table_sqls(data_dir_path)
            if not ddl_sqls:
                logging.error("no valid sql file under directory: %s", data_dir_path)

            for sql_dict in ddl_sqls:
                sql_file_path = os.path.join(data_dir_path, sql_dict["file_path"])
                res = self.lib.execute_sql(sql_dict["sql"], "ddl")
                if res is None:
                    logging.error("failed to create table. sql: %s", sql_file_path)

                if not res["status"]:
                    logging.warn("create table error. sql: %s, msg: %s", sql_file_path, res["msg"])
                else:
                    logging.info("create table success. sql: %s", sql_file_path)
        finally:
            self.close_starrocks()

    def stream_load(self, data_dir):
        data_dir_path = os.path.abspath(data_dir)
        logging.info("stream load from dir:%s", data_dir_path)
        load_data_paths = self.lib.get_load_data_paths(data_dir_path)
        if not load_data_paths:
            logging.error("no valid data files under directory: %s", data_dir_path)

        for file_name in load_data_paths:
            table_name = file_name
            file_paths = load_data_paths[table_name]

            thread_num = ConfigUtil.get_concurrency_num(table_name)

            left_num = len(file_paths)
            index = 0
            while index < len(file_paths):
                thread_num_this_cycle = min(left_num, thread_num)
                threads = list()
                for i in range(thread_num_this_cycle):
                    t = StreamLoadThread(table_name, file_paths[index])
                    t.start()
                    threads.append(t)
                    index = index + 1
                for t in threads:
                    t.join()
                left_num = left_num - thread_num_this_cycle

    def flat_insert(self):
        self.connect_starrocks()
        try:
            # use db
            starrocks_db = conf_parser.starrocks_db
            self.use_database(starrocks_db)

            # get flat insert sql
            insert_sqls = self.lib.get_flat_insert_sqls()
            for sql_dict in insert_sqls:
                print("sql: %s start" % (sql_dict["file_name"]))
                res = self.lib.execute_sql(sql_dict["sql"], "dml")
                if res is None:
                    print("sql: %s. flat insert error" % (sql_dict["file_name"]))

                if not res["status"]:
                    print("sql: %s. flat insert error, msg: %s" % (sql_dict["file_name"], res["msg"]))
                else:
                    print("sql: %s success" % (sql_dict["file_name"]))
        finally:
            self.close_starrocks()

    def parse_args(self):
        """
        parse args
        """
        parser = argparse.ArgumentParser(prog="db_table_operatio.py",
                                         description="db/table operation args parser")
        parser.add_argument("-q", "--quiet", dest="log_quiet", action="store_true",
                            default=False, help="whether not to print INFO logs")
        parser.add_argument("-v", "--verbose", dest="log_verbose", action="store_true",
                            default=False, help="whether to print DEBUG logs")
        subparsers = parser.add_subparsers(dest="operation_type", help="sub-command help")
        parser_create = subparsers.add_parser("create", help="create tables")
        self.parse_create_args(parser_create)
        parser_flat_insert = subparsers.add_parser("flat_insert", help="flat insert data")
        self.parse_flat_insert(parser_flat_insert)
        parser_stream_load = subparsers.add_parser("stream_load", help="stream load data")
        self.parse_stream_load_args(parser_stream_load)
        parser_broker_load = subparsers.add_parser("broker_load", help="broker load data")
        self.parse_broker_load_args(parser_broker_load)

        return parser

    def parse_create_args(self, parser):
        parser.add_argument("sql_dir", type=str, help="directory with create table sql files")

    def parse_flat_insert(self, parser):
        pass

    def parse_stream_load_args(self, parser):
        parser.add_argument("data_dir", type=str, help="data directory")

    def parse_broker_load_args(self, parser):
        """
        parse args for `broker load`
        """
        parser.add_argument("table_name", type=str, help="starrocks table name")
        parser.add_argument("hdfs_path", type=str, help="hdfs path")
        parser.add_argument("-c", "--columns", dest="columns", action="store",
                            type=str, default="", help="file columns")
        parser.add_argument("-cp", "--columns_from_path", dest="columns_from_path",
                            action="store", type=str, default="", help="columns from hdfs path")

    def broker_load(self, table_name, hdfs_path, columns, columns_from_path):
        """
        split small broker load jobs according to config.max_bytes_per_job
        """
        self.connect_starrocks()
        try:
            # get all files size in hdfs path
            # [(file_path, file_size), ...]
            file_list = self.lib.get_hdfs_file_infos(hdfs_path)
            if not file_list:
                raise starrocks_lib.StarrocksException("get hdfs file infos error. file list empty")

            # use db
            starrocks_db = conf_parser.starrocks_db
            self.use_database(starrocks_db)

            # get file columns
            if not columns:
                res = self.lib.execute_sql("describe %s" % (table_name), "dml")
                if res is None:
                    raise starrocks_lib.StarrocksException("table:%s get schema error" % (table_name))
                if not res["status"]:
                    raise starrocks_lib.StarrocksException("table:%s get schema error. msg: %s" \
                                                           % (table_name, res["msg"]))
                table_columns = [column_info[0] for column_info in res["result"]]
                columns = [c for c in table_columns if c not in columns_from_path]

            # split and submit broker load job
            file_num = len(file_list)
            i = 0
            while i < file_num:
                job_file_list = []
                job_file_size = 0
                while i < file_num:
                    file_info = file_list[i]
                    job_file_size = job_file_size + int(file_info[0])
                    if not job_file_list or job_file_size < conf_parser.max_bytes_per_job:
                        job_file_list.append(file_info[1])
                        i = i + 1
                    else:
                        break

                sql = self.lib.get_broker_load_sql(starrocks_db, table_name, job_file_list,
                                                   columns, columns_from_path)
                res = self.lib.execute_sql(sql, "dml")
                print("-" * 18)
                if res is None:
                    print("%s\n\nbroker load job submit error." % (sql))

                if not res["status"]:
                    print("%s\n\nbroker load job submit error. msg: %s" % (sql, res["msg"]))
                else:
                    print("%s\n\nbroker load job submit success." % (sql))
        except starrocks_lib.StarrocksException as e:
            print(e.value)
            sys.exit(-1)
        finally:
            self.close_starrocks()


if __name__ == '__main__':
    starrocks_operation = StarrocksDbTableOperation()
    args_parser = starrocks_operation.parse_args()
    args = args_parser.parse_args()

    if args.log_quiet:
        logger.LOG_LEVEL = logging.WARN
    elif args.log_verbose:
        logger.LOG_LEVEL = logging.DEBUG
    logger.init_logging(level=logger.LOG_LEVEL)
    logging.debug("args: %s", args)

    if args.operation_type == "create":
        starrocks_operation.create_db_table(args.sql_dir)
    elif args.operation_type == "stream_load":
        starrocks_operation.stream_load(args.data_dir)
    elif args.operation_type == "flat_insert":
        starrocks_operation.flat_insert()
    elif args.operation_type == "broker_load":
        columns = [c.strip() for c in args.columns.split(",")] if args.columns else []
        columns_from_path = [c.strip() for c in args.columns_from_path.split(",")]\
            if args.columns_from_path else []
        starrocks_operation.broker_load(args.table_name, args.hdfs_path, columns, columns_from_path)
    elif not args.operation_type:
        logging.error("should specify the operation type.")
        args_parser.print_help()
    else:
        logging.error("error operation type=%s", args.operation_type)
