#!/bin/bash

data_dir=$1
if [[ ! -d "${data_dir}" ]];then
    echo "[ERROR] data_dir for generated data not specified"
    exit 1
fi

for file in $(ls "${data_dir}")
do
    file_path=${data_dir}/${file}
    echo "[INFO] sed file:${file_path}"
    # nohup sed -i 's/|$//g' ${file_path} &
    sed -i 's/|$//g' "${file_path}"
done

