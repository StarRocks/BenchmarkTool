#!/usr/bin/env python
# -- coding: utf-8 --
import os

BENCHMARKS = ["ssb", "tpch"]
# the default benchmark to test
BENCHMARK = "tpch"

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
# StarRocks's conf file
STARROCKS_CONF = os.path.join(PROJECT_ROOT_PATH, "conf/starrocks.conf")
# the root directory of all SQL
SQL_ROOT = os.path.join(PROJECT_ROOT_PATH, "sql")
# the result directory of all result
RESULT_ROOT = os.path.join(PROJECT_ROOT_PATH, "result")

################################################################################
# load config info
TPCH_CONCURRENCY_LOAD_CONFIG = {
    "lineitem": 10,
    "orders": 5
}

# concurrency for big table to load in parallel
CONCURRENCY_LOAD_CONFIG = {
    "tpch": TPCH_CONCURRENCY_LOAD_CONFIG
}
