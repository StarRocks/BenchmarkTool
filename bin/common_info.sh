#!/bin/sh

_CONFIG_DIR_=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

PYTHON=python3
PROJECT_ROOT=$(cd "${_CONFIG_DIR_}"/.. && pwd)
SRC_PATH="${PROJECT_ROOT}"/src
THIRDPARTY_PATH="${PROJECT_ROOT}"/thirdparty
