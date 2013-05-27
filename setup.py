#!/usr/bin/env python

import os
import sys

import geoip2

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ['geoip2']

requirements = [i.strip() for i in open("requirements.txt").readlines()]

if sys.version_info[0] == 2 or (sys.version_info[0] == 3
                                and sys.version_info[1] < 3):
    requirements.append('ipaddr')

setup(
    name='geoip2',
    version=geoip2.__version__,
    description='MaxMind GeoIP2 API',
    long_description=open('README.rst').read(),
    author='Gregory Oschwald',
    author_email='goschwald@maxmind.com',
    url='http://www.maxmind.com/',
    bugtrack_url='https://github.com/maxmind/GeoIP2-python/issues',
    packages=['geoip2'],
    package_data={'': ['LICENSE'] },
    package_dir={'geoip2': 'geoip2'},
    include_package_data=True,
    install_requires=requirements,
    test_suite="tests",
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet',
    ),
)
