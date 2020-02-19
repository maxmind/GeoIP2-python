#!/bin/bash

set -eux

diff=$(black --check .)

if [[ $? != 0 ]]; then
    echo "black failed to run."
    echo "$diff"
    exit $?
elif [[ $diff ]]; then
    echo "$diff"
    exit 1
else
    exit 0
fi
