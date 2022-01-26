drop table if exists partsupp;
CREATE TABLE partsupp ( ps_partkey          int NOT NULL,
                             ps_suppkey     int NOT NULL,
                             ps_availqty    int NOT NULL,
                             ps_supplycost  decimal(15, 2)  NOT NULL,
                             ps_comment     VARCHAR(199) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`ps_partkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`ps_partkey`) BUCKETS 24
PROPERTIES (
    "replication_num" = "1",
    "in_memory" = "false",
    "storage_format" = "DEFAULT",
    "colocate_with" = "group_tpch_100p"
);