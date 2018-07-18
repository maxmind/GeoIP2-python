#!/bin/bash

set -eux

python setup.py install
pylint geoip2
