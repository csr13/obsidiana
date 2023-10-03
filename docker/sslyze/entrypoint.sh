#!/bin/sh

set -x

for argument in ${@}; do
    if [ $argument = "--help" ]; then
        python3 -m sslyze --help
        exit 0
    fi;
done

args_array="$@"

python3 -m sslyze $args_array > out.json && python3 -m json.tool out.json
