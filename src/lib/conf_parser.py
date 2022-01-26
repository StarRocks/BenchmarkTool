#!/usr/bin/env python
# -- coding: utf-8 --
import configparser
import os
import sys

import config.config as project_config

if not os.path.exists(project_config.STARROCKS_CONF):
    print("StarRocks config file not exist. file: %s" % project_config.STARROCKS_CONF)
    sys.exit()
config = configparser.ConfigParser()
config.read(project_config.STARROCKS_CONF)

# starrocks config
starrocks_mysql_host = config.get("starrocks", "mysql_host")
starrocks_mysql_port = config.get("starrocks", "mysql_port")
starrocks_mysql_user = config.get("starrocks", "mysql_user")
starrocks_mysql_password = config.get("starrocks", "mysql_password")
starrocks_db = config.get("starrocks", "database")
starrocks_http_port = config.get("starrocks", "http_port")
sleep_ms = config.get("starrocks", "sleep_ms")

# optional
parallel_num_string = config.get("starrocks", "parallel_num", fallback="1")
parallel_num_list = parallel_num_string.split(",")
concurrency_num_string = config.get("starrocks", "concurrency_num", fallback="1")
concurrency_num_list = concurrency_num_string.split(",")
num_of_queries = config.getint("starrocks", "num_of_queries", fallback=1)

# broker config
broker_name = config.get("broker_load", "broker")
broker_username = config.get("broker_load", "broker_username")
broker_password = config.get("broker_load", "broker_password")
hadoop_home = config.get("broker_load", "hadoop_home")
max_bytes_per_job = config.getint("broker_load", "max_bytes_per_job", fallback=524288000)
file_format = config.get("broker_load", "file_format", fallback="orc")
column_separator = config.get("broker_load", "column_separator", fallback="\t")
max_filter_ratio = config.get("broker_load", "max_filter_ratio", fallback="0")
timeout = config.get("broker_load", "timeout", fallback="14400")
