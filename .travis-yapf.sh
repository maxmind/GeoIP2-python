#!/bin/bash

set -eux

diff=$(yapf -rd geoip2 tests)

if [[ $? != 0 ]]; then
    echo "yapf failed to run."
    echo "$diff"
    exit $?
elif [[ $diff ]]; then
    echo "$diff"
    exit 1
else
    exit 0
fi
