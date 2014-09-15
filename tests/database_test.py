#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
sys.path.append('..')

import geoip2.database

if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

if sys.version_info[0] == 2:
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp


class TestReader(unittest.TestCase):

    def test_default_locale(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        record = reader.city('81.2.69.160')

        self.assertEqual(record.country.name, 'United Kingdom')
        reader.close()

    def test_language_list(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-Country-Test.mmdb',
            ['xx', 'ru', 'pt-BR', 'es', 'en'])
        record = reader.country('81.2.69.160')

        self.assertEqual(record.country.name, 'Великобритания')
        reader.close()

    def test_has_ip_address(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-Country-Test.mmdb')
        record = reader.country('81.2.69.160')
        self.assertEqual(record.traits.ip_address, '81.2.69.160')
        reader.close()

    def test_unknown_address(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        with self.assertRaisesRegex(geoip2.errors.AddressNotFoundError,
                                    'The address 10.10.10.10 is not in the '
                                    'database.'):
            reader.city('10.10.10.10')
        reader.close()

    def test_wrong_database(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        with self.assertRaisesRegex(TypeError,
                                    'The country method cannot be used with '
                                    'the GeoIP2-City database'):
            reader.country('1.1.1.1')
        reader.close()

    def test_invalid_address(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        with self.assertRaisesRegex(ValueError,
                                    "u?'invalid' does not appear to be an "
                                    "IPv4 or IPv6 address"):
            reader.city('invalid')
        reader.close()

    def test_connection_type(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-Connection-Type-Test.mmdb')
        ip_address = '1.0.1.0'

        record = reader.connection_type(ip_address)
        self.assertEqual(record.connection_type, 'Cable/DSL')
        self.assertEqual(record.ip_address, ip_address)
        reader.close()

    def test_domain(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-Domain-Test.mmdb')

        ip_address = '1.2.0.0'
        record = reader.domain(ip_address)
        self.assertEqual(record.domain, 'maxmind.com')
        self.assertEqual(record.ip_address, ip_address)

        reader.close()

    def test_isp(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-ISP-Test.mmdb')

        ip_address = '1.128.0.0'
        record = reader.isp(ip_address)
        self.assertEqual(record.autonomous_system_number, 1221)
        self.assertEqual(record.autonomous_system_organization,
                         'Telstra Pty Ltd')
        self.assertEqual(record.isp, 'Telstra Internet')
        self.assertEqual(record.organization, 'Telstra Internet')
        self.assertEqual(record.ip_address, ip_address)

        reader.close()
