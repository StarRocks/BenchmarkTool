#!/usr/bin/env python
# -- coding: utf-8 --
import argparse
import logging
import re
import subprocess
import sys
import time

from lib import conf_parser
from lib import starrocks_lib
from utility import logger

MYSQLSLAP_RESULT_STR = "Average number of seconds to run all queries"
MYSQLSLAP_ERROR = "Error"


class StarrocksBenchmark(object):
    def __init__(self):
        self.lib = starrocks_lib.StarrocksLib()

    def parse_args(self):
        """
        parse args
        """
        parser = argparse.ArgumentParser(description="benchmark args parser")
        parser.add_argument("-p", "--performance", dest="performance", action="store_true",
                            default=False, help="test performance")
        parser.add_argument("-c", "--check_result", dest="check_result", action="store_true",
                            default=False, help="check result")
        parser.add_argument("-s", "--scale", dest="scale", type=int, action="store",
                            default=100, help="data scale")
        parser.add_argument("-d", "--dataset", type=str, action="store",
                            default="", help="specify a dataset to test."
                                             " otherwise the sql files under <query> directory will be tested")
        parser.add_argument("-S", "--sql_file", type=str, action="store",
                            default="", help="you cant specify a single query sql file to test."
                                             " otherwise all sql files included")
        parser.add_argument("-q", "--quiet", dest="log_quiet", action="store_true",
                            default=False, help="whether not to print INFO logs")
        parser.add_argument("-v", "--verbose", dest="log_verbose", action="store_true",
                            default=False, help="whether to print DEBUG logs")
        return parser

    def connect_starrocks(self):
        self.lib.connect()

    def close_starrocks(self):
        self.lib.close()

    def use_database(self, db_name):
        self.lib.use_database(db_name)

    def sort_sql_list(self, sql_info_list):
        """
        order by q1, q2, ... q10
        """
        for sql_info_dict in sql_info_list:
            digit_part = re.sub(r"\D", "", sql_info_dict["file_name"])
            sql_info_dict["index"] = int(digit_part) if digit_part else 0
        sql_info_list.sort(key=lambda x: x["index"])

    def get_test_sql_dirs(self, sql_dir_name):
        """
        get sub directories under <query> directory
        :params sql_dir_name
            <empty>: for `.` (the <query> directory)
            all: for all the sub directories under <query> directory
            otherwise the specified directory under <query> directory
        """
        test_sql_dirs = []
        # get all query sql dirs
        sql_dirs = self.lib.get_query_sql_dirs()
        # check user assigned sql dir
        if not sql_dir_name or sql_dir_name == ".":
            test_sql_dirs.append(".")
        elif sql_dir_name == "all":
            test_sql_dirs.extend(sql_dirs)
        elif sql_dir_name in sql_dirs:
            test_sql_dirs.append(sql_dir_name)
        else:
            logging.info("can not find dataset:%s in directory:%s", sql_dir_name, sql_dirs)
            valid_dirs = [".", "all"] + sql_dirs
            logging.error("wrong dataset: %s, should be one of %s", sql_dir_name, valid_dirs)
        return test_sql_dirs

    def test_parallel_performance(self, sql_dir_name, sql_file=None):
        """ parallel performance """

        self.connect_starrocks()
        try:
            # use db
            db_name = conf_parser.starrocks_db
            self.use_database(db_name)

            # check sql dirs, there may be serveral directories for `all`
            test_sql_dirs = self.get_test_sql_dirs(sql_dir_name)
            logging.info("test sql in dirs:[%s]", ", ".join(test_sql_dirs))

            # execute query
            # sql\time(ms)\parallel_num   1   2   3
            # sql1  10  20  30
            # sql2  11  21  31
            for sql_dir in test_sql_dirs:
                sql_list = self.lib.get_query_table_sqls(sql_dir)
                # logging.debug("get sql files under sql_dir:%s", sql_list)
                # sort sql file for determinated test
                self.sort_sql_list(sql_list)
                for concurrency_num in conf_parser.concurrency_num_list:
                    print("------ dataset: %s, concurrency: %s ------" % (sql_dir, concurrency_num))
                    print("sql\\time(ms)\\parallel_num\t%s" % ("\t".join(conf_parser.parallel_num_list)))
                    sql_file_exec_count = 0
                    for sql_dict in sql_list:
                        sql_file_name = sql_dict["file_name"]  # file name without extension `.sql`
                        if sql_file and sql_file != sql_file_name:
                            logging.debug("Not specified sql file, skip it. file='%s'", sql_file_name)
                            continue
                        else:
                            logging.debug("Run sql file. file='%s'", sql_file_name)

                        sql_file_exec_count += 1
                        result = [sql_file_name]
                        for parallel_num in conf_parser.parallel_num_list:
                            query_dict = {"parallel_num": parallel_num,
                                          "concurrency": concurrency_num,
                                          "num_of_queries": conf_parser.num_of_queries,
                                          "database": db_name,
                                          "sql": sql_dict["sql"]}

                            cmd = self.lib.get_parallel_cmd(query_dict)
                            logging.debug("Run sql file. cmd={%s}", cmd)
                            begin_time = time.time()
                            res, output = subprocess.getstatusoutput(cmd)
                            end_time = time.time()
                            # logging.debug("res=%s, output={%s}", res, output)
                            if res != 0 or (output and (MYSQLSLAP_RESULT_STR not in output
                                                        or MYSQLSLAP_ERROR in output)):
                                logging.error("exec sql error. sql: %s, output: \n%s", sql_file_name, output)
                                result.append("-")
                            else:
                                time_cost = (int(round(end_time * 1000)) - int(round(begin_time * 1000))) \
                                            / int(1 if conf_parser.num_of_queries < int(concurrency_num)
                                                  else conf_parser.num_of_queries / int(concurrency_num))
                                result.append(str(time_cost))
                            time.sleep(int(conf_parser.sleep_ms) / 1000.0)
                            # print(begin_time, end_time, time_cost, output)

                        print("\t".join(result))
                    logging.info("run %s sql files at concurrency:%s", sql_file_exec_count, concurrency_num)
        finally:
            self.close_starrocks()

    def check_results(self, sql_dir_name, scale):
        self.connect_starrocks()
        try:
            # use db
            self.use_database(conf_parser.starrocks_db)

            # check sql dir args
            test_sql_dirs = self.get_test_sql_dirs(sql_dir_name)

            # execute query and diff
            for sql_dir in test_sql_dirs:
                print("------ %s ------" % sql_dir)
                sql_list = self.lib.get_query_table_sqls(sql_dir)
                self.sort_sql_list(sql_list)
                for sql_dict in sql_list:
                    sql_file = sql_dict["file_name"]
                    query_res = self.lib.execute_sql(sql_dict["sql"], "dml")
                    # logging.debug("execute sql. sql_info=%s, result=%s", sql_dict, query_res)
                    if query_res is None:
                        print("sql: %s. exec sql error." % sql_file)
                        continue

                    if not query_res["status"]:
                        print("sql: %s. exec sql error, msg: %s" % (sql_file, query_res["msg"]))
                        continue

                    # get base result from file
                    base_result = self.lib.get_query_base_result(sql_dir, scale, sql_file)
                    if base_result is None:
                        logging.error("sql: %s, scale: %d. check result error, msg: base result file not exist",
                                      sql_file, scale)
                        query_result = query_res["result"]
                        if query_result:
                            logging.debug("sql file: %s, query result: %s", sql_file, query_result)
                        else:
                            logging.error("no query result.")

                        continue

                    # diff query result
                    # row count
                    query_result = query_res["result"]
                    if len(query_result) != len(base_result):
                        print("sql: %s. check result error, row count is different, base: %s, query: %s"
                              % (sql_file, len(base_result), len(query_result)))
                        continue

                    # row
                    i = 0
                    is_same = True
                    for line in query_res["result"]:
                        normalize_line = [str(col) if col is not None else "NULL" for col in line]
                        normalize_line_str = "\t".join(normalize_line)
                        base_result_line_str = base_result[i]
                        i = i + 1
                        if normalize_line_str != base_result_line_str:
                            is_same = False
                            print("sql: %s. check result error, row content is different, base: (%s), query: (%s)"
                                  % (sql_file, base_result_line_str, normalize_line_str))
                            break
                    if not is_same:
                        continue

                    print("sql: %s ok" % sql_file)
        finally:
            self.close_starrocks()


if __name__ == '__main__':
    benchmark = StarrocksBenchmark()
    args_parser = benchmark.parse_args()
    args = args_parser.parse_args()

    if args.log_quiet:
        logger.LOG_LEVEL = logging.WARN
    elif args.log_verbose:
        logger.LOG_LEVEL = logging.DEBUG
    logger.init_logging(level=logger.LOG_LEVEL)
    logging.info("benchmark args:%s", args)

    if args.performance and args.check_result:
        print("-c and -p should not be assigned at the same time.\n")
        args_parser.print_help()
        sys.exit(-1)
    elif args.performance:
        benchmark.test_parallel_performance(args.dataset, args.sql_file)
    elif args.check_result:
        benchmark.check_results(args.dataset, args.scale)
    else:
        print("missing -c or -p args.\n")
        args_parser.print_help()
        sys.exit(-1)
