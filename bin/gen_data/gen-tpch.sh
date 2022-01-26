#!/bin/bash

# usage for the script
usage()
{
    echo -e "$(basename "$0") \033[49;32;1m data_size data_dir \033[0m"
    echo -e '\033[1m[USAGE]\033[0m'
    echo -e '    Gens tpch data at the specified size under the specified data directory.'
    echo -e '\033[1m[OPTIONS]\033[0m'
    echo -e '    \033[49;32;1m-h\033[0m : print this help.'
    echo -e '    \033[49;32;1mdata_size\033[0m : 1 for 1GB, 2 for 2GB, ...'
    echo -e '    \033[49;32;1mdata_dir\033[0m : data directory to store all the generated table data,'\
            'it will be created if not exist'
    echo -e '\033[1m[RETURN]\033[0m'
}

if [[ $# -lt 2 ]] || [[ "$1" == "-h" ]]; then
    usage
    exit 1
fi

_GEN_FILE_DIR_=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

. "${_GEN_FILE_DIR_}"/../common_info.sh

dbgen_path=${PROJECT_ROOT}/thirdparty/tpch-dbgen
# max chunk size of a file, unit: GB
FILE_CHUNK_SIZE=5


################################################################################
# data size, unit: GB
size=$1
# data_dir for generated data
data_dir=$2


if [[ -z "${size}" ]]; then
    size=1
else
    size=$((size + 0))
fi

# refine the data_dir to be a absolute path
if [[ -z "${data_dir}" ]];then
    data_dir=$(pwd)
elif [[ ! "${data_dir:0:1}" == "/" ]];then
    data_dir="$(pwd)/${data_dir}"
fi
mkdir -p "${data_dir}"

echo "[INFO] gen ${size}GB data under ${data_dir}"


################################################################################
table_names=("customer" "lineitem" "nation" "orders" "parts" "partsupp" "region" "suppliers")
tables=(     "c"        "L"        "n"      "O"      "P"     "S"        "r"      "s")

# chunk number for lineitem
pl=$((size / FILE_CHUNK_SIZE))
# chunk numbers for all tables
parts=($((pl / 20))
       $((pl / 1))
       1
       $((pl / 5))
       $((pl / 20))
       $((pl / 5))
       1
       $((pl / 500))
)


# separate data to multiple parts
echo "[INFO] generate data..." >&2
cd "${data_dir}" || exit

for ((ti=0; ti<${#tables[@]}; ti++))
do
    table_name=${table_names[$ti]}
    table=${tables[$ti]}
    part_num=${parts[$ti]}
    echo "[INFO] gen data of table: ${table_name}" >&2
    if [[ ${part_num} -le 0 ]];then
        part_num=1
    fi

    for i in $(seq 1 ${part_num})
    do
        if [[ ${part_num} -gt 1 ]];then
            echo "[INFO] gen <$i>th part data of table: ${table_name}"
            #nohup ${dbgen_path}/dbgen -s 1 -C 10 -S $i -b ${dbgen_path}/dists.dss -T S &
            "${dbgen_path}"/dbgen -s ${size} -C ${part_num} -S $i -b "${dbgen_path}"/dists.dss -T ${table}
        else
            "${dbgen_path}"/dbgen -s ${size} -C 1 -b "${dbgen_path}"/dists.dss -T "${table}"
        fi
    done
done
cd "${_GEN_FILE_DIR_}" || exit

# sed to remove the end `|`
echo "[INFO] refine the data in ${data_dir}" >&2
"${_GEN_FILE_DIR_}"/clean-tpch.sh "${data_dir}"

