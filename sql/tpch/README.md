# sql files for tpch


## ddl


### ddl.original

The original create-table statement, mainly with the same column order to the data gened.

`create table` in other directories such like ddl_100, ddl_1000 may have different column orders.
The main reason is for better query performance.


### ddl_100

`create table` for 100GB.


### ddl_100.single_table

`create table` for 100GB, but with single table creation every file.

    
### ddl_1000

`create table` for 1TB.
Tables may be with larger bucket number than ddl_100.


## query

query sqls.
