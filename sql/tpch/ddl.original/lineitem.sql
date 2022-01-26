CREATE TABLE lineitem ( l_orderkey    bigint NOT NULL,
                             l_partkey     bigint NOT NULL,
                             l_suppkey     integer not null,
                             l_linenumber  integer not null,
                             l_quantity    double NOT NULL,
                             l_extendedprice  double NOT NULL,
                             l_discount    double NOT NULL,
                             l_tax         double NOT NULL,
                             l_returnflag  CHAR(1) NOT NULL,
                             l_linestatus  CHAR(1) NOT NULL,
                             l_shipdate    DATE NOT NULL,
                             l_commitdate  DATE NOT NULL,
                             l_receiptdate DATE NOT NULL,
                             l_shipinstruct CHAR(25) NOT NULL,
                             l_shipmode     CHAR(10) NOT NULL,
                             l_comment      VARCHAR(44) NOT NULL)
ENGINE=OLAP
DUPLICATE KEY(`l_orderkey`)
COMMENT "OLAP"
PARTITION BY RANGE(`l_shipdate`)
(
PARTITION p1992 VALUES LESS THAN ("19930101"),
PARTITION p1993 VALUES LESS THAN ("19940101"),
PARTITION p1994 VALUES LESS THAN ("19950101"),
PARTITION p1995 VALUES LESS THAN ("19960101"),
PARTITION p1996 VALUES LESS THAN ("19970101"),
PARTITION p1997 VALUES LESS THAN ("19980101"),
PARTITION p1998 VALUES LESS THAN ("19990101")
)
DISTRIBUTED BY HASH(`l_orderkey`) BUCKETS 96
PARTITIONNS
PROPERTIES (
"replication_num" = "1",
"in_memory" = "false",
"storage_format" = "DEFAULT",
"colocated_with" = "tpch1"
);
