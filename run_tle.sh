#!/bin/bash

# Get to a predictable directory, the directory of this script
cd "$(dirname "$0")"

[ -e environment ] && . ./environment

while true; do
    # git pull
    # poetry install
    # FONTCONFIG_FILE=$PWD/extra/fonts.conf poetry run python -m tle

    poetry run python3.8 -m tle
    # (( $? == 0 )) && break

    echo '==================================================================='
    echo '=                       Restarting                                ='
    echo '==================================================================='
done