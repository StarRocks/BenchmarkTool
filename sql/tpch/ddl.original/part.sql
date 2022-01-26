CREATE TABLE part  ( p_partkey          bigint NOT NULL,
                          p_name        VARCHAR(55) NOT NULL,
                          p_mfgr        CHAR(25) NOT NULL,
                          p_brand       CHAR(10) NOT NULL,
                          p_type        VARCHAR(25) NOT NULL,
                          p_size        INTEGER NOT NULL,
                          p_container   CHAR(10) NOT NULL,
                          p_retailprice double NOT NULL,
                          p_comment     VARCHAR(23) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`p_partkey`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`p_partkey`) BUCKETS 10
PROPERTIES (
"replication_num" = "1",
"in_memory" = "false",
"storage_format" = "DEFAULT"
);
