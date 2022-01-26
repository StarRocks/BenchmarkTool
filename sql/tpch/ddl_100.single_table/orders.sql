drop table if exists orders;
CREATE TABLE orders  ( o_orderkey       int NOT NULL,
                       o_orderdate      DATE NOT NULL,
                       o_custkey        int NOT NULL,
                       o_orderstatus    VARCHAR(1) NOT NULL,
                       o_totalprice     decimal(15, 2) NOT NULL,
                       o_orderpriority  VARCHAR(15) NOT NULL,
                       o_clerk          VARCHAR(15) NOT NULL,
                       o_shippriority   int NOT NULL,
                       o_comment        VARCHAR(79) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`o_orderkey`, `o_orderdate`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`o_orderkey`) BUCKETS 96
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT",
    "colocate_with" = "group_tpch_100"
);