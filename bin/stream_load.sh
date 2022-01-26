#!/bin/sh

BIN_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

. "${BIN_PATH}"/common_info.sh

$PYTHON "${SRC_PATH}"/db_table_operation.py stream_load "$@"
