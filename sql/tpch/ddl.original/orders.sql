CREATE TABLE orders  ( o_orderkey       bigint NOT NULL,
                       o_custkey        bigint NOT NULL,
                       o_orderstatus    CHAR(1) NOT NULL,
                       o_totalprice     double NOT NULL,
                       o_orderdate      DATE NOT NULL,
                       o_orderpriority  CHAR(15) NOT NULL,  
                       o_clerk          CHAR(15) NOT NULL, 
                       o_shippriority   INTEGER NOT NULL,
                       o_comment        VARCHAR(79) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`o_orderkey`)
PARTITION BY RANGE(`o_orderdate`)
(
PARTITION p1992 VALUES LESS THAN ("19930101"),
PARTITION p1993 VALUES LESS THAN ("19940101"),
PARTITION p1994 VALUES LESS THAN ("19950101"),
PARTITION p1995 VALUES LESS THAN ("19960101"),
PARTITION p1996 VALUES LESS THAN ("19970101"),
PARTITION p1997 VALUES LESS THAN ("19980101"),
PARTITION p1998 VALUES LESS THAN ("19990101")
)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`o_orderkey`) BUCKETS 96
PROPERTIES (
"replication_num" = "1",
"in_memory" = "false",
"storage_format" = "DEFAULT",
"colocated_with" = "tpch1"
);
