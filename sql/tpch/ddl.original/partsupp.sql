CREATE TABLE partsupp ( ps_partkey          bigint NOT NULL,
                             ps_suppkey     bigint NOT NULL,
                             ps_availqty    INTEGER NOT NULL,
                             ps_supplycost  double  NOT NULL,
                             ps_comment     VARCHAR(199) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`ps_partkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`ps_partkey`) BUCKETS 10
PROPERTIES (
"replication_num" = "1",
"in_memory" = "false",
"storage_format" = "DEFAULT"
);
