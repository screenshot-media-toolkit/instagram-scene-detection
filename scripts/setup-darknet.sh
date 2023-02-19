#!/usr/bin/env bash

darknet_dir="darknet-darknet_yolo_v3_optimal"

# download and unzip the darknet package if not present
if [ ! -d "${darknet_dir}" ]; then
    wget https://github.com/AlexeyAB/darknet/archive/refs/tags/darknet_yolo_v3_optimal.zip
    unzip darknet_yolo_v3_optimal.zip
fi

cd "${darknet_dir}"

sed -i'.bak' -e 's/OPENMP=[01]/OPENMP=1/g' -e 's/LIBSO=[01]/LIBSO=1/g' Makefile

make

cp libdarknet.so ..