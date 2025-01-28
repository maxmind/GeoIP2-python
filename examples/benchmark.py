#!/usr/bin/python


import argparse
import contextlib
import random
import socket
import struct
import timeit

import geoip2.database

parser = argparse.ArgumentParser(description="Benchmark maxminddb.")
parser.add_argument("--count", default=250000, type=int, help="number of lookups")
parser.add_argument("--mode", default=0, type=int, help="reader mode to use")
parser.add_argument("--file", default="GeoIP2-City.mmdb", help="path to mmdb file")

args = parser.parse_args()

reader = geoip2.database.Reader(args.file, mode=args.mode)


def lookup_ip_address() -> None:
    ip = socket.inet_ntoa(struct.pack("!L", random.getrandbits(32)))
    with contextlib.suppress(geoip2.errors.AddressNotFoundError):
        reader.city(str(ip))


elapsed = timeit.timeit(
    "lookup_ip_address()",
    setup="from __main__ import lookup_ip_address",
    number=args.count,
)

print(args.count / elapsed, "lookups per second")
