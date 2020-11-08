#!/usr/bin/env python

import codecs
import os
import sys

import geoip2

from setuptools import setup

packages = ["geoip2"]

requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="geoip2",
    version=geoip2.__version__,
    description="MaxMind GeoIP2 API",
    long_description=codecs.open("README.rst", "r", "utf-8").read(),
    author="Gregory Oschwald",
    author_email="goschwald@maxmind.com",
    url="http://www.maxmind.com/",
    packages=["geoip2"],
    package_data={"": ["LICENSE"], "geoip2": ["py.typed"]},
    package_dir={"geoip2": "geoip2"},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "all": ["requests>=2.14.0,<3.0.0", "aiohttp>=3.6.2,<4.0.0"],
        "requests": "requests>=2.14.0,<3.0.0",
        "aiohttp": "aiohttp>=3.6.2,<4.0.0",
    },
    tests_require=["mocket>=3.8.9"],
    test_suite="tests",
    license=geoip2.__license__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet",
    ],
)
