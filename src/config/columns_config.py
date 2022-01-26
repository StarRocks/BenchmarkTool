#!/usr/bin/env python
# -- coding: utf-8 --

# you can specify the column order if the column order in dest table
# is different from the original data columns.
# directly set the original columns in the array
# if empty or not set for a table, it will keep original
tpch_columns = {
    "customer": ["C_CUSTKEY",
                 "C_NAME",
                 "C_ADDRESS",
                 "C_NATIONKEY",
                 "C_PHONE",
                 "C_ACCTBAL",
                 "C_MKTSEGMENT",
                 "C_COMMENT"],
    "lineitem": ["l_orderkey",
                 "l_partkey",
                 "l_suppkey",
                 "l_linenumber",
                 "l_quantity",
                 "l_extendedprice",
                 "l_discount",
                 "l_tax",
                 "l_returnflag",
                 "l_linestatus",
                 "l_shipdate",
                 "l_commitdate",
                 "l_receiptdate",
                 "l_shipinstruct",
                 "l_shipmode",
                 "l_comment"],
    "nation": [],
    "orders": ["o_orderkey",
               "o_custkey",
               "o_orderstatus",
               "o_totalprice",
               "o_orderdate",
               "o_orderpriority",
               "o_clerk",
               "o_shippriority",
               "o_comment"],
    "part": ["p_partkey",
             "p_name",
             "p_mfgr",
             "p_brand",
             "p_type",
             "p_size",
             "p_container",
             "p_retailprice",
             "p_comment"],
    "partsupp": ["ps_partkey",
                 "ps_suppkey",
                 "ps_availqty",
                 "ps_supplycost",
                 "ps_comment"],
    "region": [],
    "supplier": ["S_SUPPKEY",
                 "S_NAME",
                 "S_ADDRESS",
                 "S_NATIONKEY",
                 "S_PHONE",
                 "S_ACCTBAL",
                 "S_COMMENT"]
}

columns = {
    "tpch": tpch_columns
}
