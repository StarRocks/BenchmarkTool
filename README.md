# Benchmark tool

Benchmark tool to test StarRocks using several benchmarks.

## Tool description

### Requirements

* python3
* python libraries: pymysql

   using commands: `pip3 install pymysql`

### Project directories

* `bin`: directory for some scripts
* `conf`: directory for conf files
* `result`: directory to store query results
* `sql`: directory for all SQL files, there will be some sub-directories for different benchmarks
  * `tpch`: tpch benchmark SQL files including `create`, `load` and `query`
  * `ssb`: ssb benchmark SQL files including `create`, `load` and `query`
* `src`: directory for tool codes
* `thirdparty`: directory to store third party modules, such as dbgen for tpch, ssb

### Scripts

All the scripts under `bin` directory:

* `gen_data`: tools to gen data like tpch, ssb, ...
  * **gen-tpch.sh**: script to gen tpch data
  * **gen-ssb.sh**: script to gen ssb data
* **create_db_table.sh**: script to create tables
* **stream_load.sh**: script to load data into StarRocks using `stream load`
* **broker_load.sh**: script to load data into StarRocks using `broker load` (not finished yet)
* **flat_insert.sh**: script to load data into StarRocks using `insert into` (not finished yet)
* **benchmark.sh**: script to test the performance or check the result correctness

### Test steps

1. Make sure the `Requirements` finished.
2. Compile the dbgen tool under `thirdparty` directory that you want.
    * tpch's `dbgen` binary is directly provided, we will add `Makefile` later.
3. Make sure a StarRocks cluster is ready,
   and you know the configuration that will be used in `conf/starrocks.conf` file.
4. Choose the benchmark you want, follow the specified steps bellow.

## SSB (Star Schema benchmark)

> not finished yet

## TPC-H benchmark

1. Configure the StarRocks cluster info in file `conf/starrocks.conf`

    You should check and modify the IP, port, database info if needed.

    You can change other parameters if know them well.

2. Create tables

    ```bash
    # create tables for 100GB data
    ./bin/create_db_table.sh ddl_100
    ```

    You can specify other directory name (under sql/tpch directory)
    in which there are `create table` SQL files.
    There are some subtle differences between the same table's SQL files under different directories,
    like: different bucket size, different column order, which are for performance only.
    You can directly use `create table` SQL files under ddl_100 for smaller data, such as 1GB.

3. Generate data

    ```bash
    # generate 100GB data under the `data_100` directory
    ./bin/gen_data/gen-tpch.sh 100 data_100

    # generate 1TB data under the `data_1T` directory
    ./bin/gen_data/gen-tpch.sh 1000 data_1T
    ```

    You can change `100` to `1` to gen data quickly for test.
    Such as: `./bin/gen_data/gen-tpch.sh 1 data_1G`

    You can use absolute or relative directory path to store generated data.
    Such as: `./bin/gen_data/gen-tpch.sh 1 data/data_1G-2`

4. Load data using stream load

    ```bash
    # load 100GB data into StarRocks
    ./bin/stream_load.sh data_100
    ```

    `data_100` is the directory path with data you generated.
    You can either specify a absolute path or a relative path.

5. Test the performance

    ```bash
    ./bin/benchmark.sh -v -p -d tpch
    ```

    See more information with `./bin/benchmark.sh -h`

6. Check the result

    ```bash
    ./bin/benchmark.sh -v -c -d tpch
    ```

    Recently, you can check the result in the logs.
    (The expected result hasn't been put in the `result` directory yet)

## Project directories in detail

It's for developers or testers.
You can add in more benchmarks, including **data gen** tool, **SQL query** file, etc.

### SQL directory

All SQL files are under the `sql` directory.
There are several sub-directories for different benchmarks, one benchmark a directory.
Such as `ssb`, `tpch`, `tpcds`, etc.

Under each benchmark directory (just take the `tpch` directory for an example), there are serveral kinds of directories:

* `ddl*`: There is usually a `***_create.sql` file to create all the tables.
    Different directories are for different data size with some different `create table` properties.

    See detail info in [tpch-README](sql/tpch/README.md)

* `query`: There may be several sub-directories for different query purposes.

    Take the `ssb` benchmark for an example, there are `ssb`, `ssb-flat`, `ssb-low_cardinality` sub-directories,
    where the `ssb-flat` is for queries on the flatten table `lineorder_flat`,
    and the `ssb-low_cardinality` is for queries in **low cardinality** situation.

* `insert`: We can insert data into a flatten **wide table** from other tables, mainly for `ssb` benchmark recently.

### Thirdparty directory

Tools to generate data for different benchmarks.
A simple copy for each.

> Add links here (TODO)
