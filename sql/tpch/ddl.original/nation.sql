CREATE TABLE `nation` (
  `n_nationkey` int(11) NOT NULL COMMENT "",
  `n_name`      char(25) NOT NULL COMMENT "",
  `n_regionkey` int(11) NOT NULL COMMENT "",
  `n_comment`   varchar(152) NULL COMMENT ""
) ENGINE=OLAP
DUPLICATE KEY(`N_NATIONKEY`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`N_NATIONKEY`) BUCKETS 1
PROPERTIES (
"replication_num" = "3",
"in_memory" = "false",
"storage_format" = "DEFAULT"
);
