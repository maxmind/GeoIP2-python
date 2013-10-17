#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
sys.path.append('..')

import geoip2.database
import geoip2.errors

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
            'tests/data/test-data/GeoIP2-City-Test.mmdb',
            ['xx', 'ru', 'pt-BR', 'es', 'en'])
        record = reader.country('81.2.69.160')

        self.assertEqual(record.country.name, 'Великобритания')
        reader.close()

    def test_has_ip_address(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        record = reader.country('81.2.69.160')
        record = reader.omni('81.2.69.160')
        self.assertEqual(record.traits.ip_address, '81.2.69.160')
        reader.close()

    def test_unknown_address(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        with self.assertRaisesRegex(geoip2.errors.AddressNotFoundError,
                                    'The address 10.10.10.10 is not in the '
                                    'database.'):
            reader.city_isp_org('10.10.10.10')
        reader.close()

    def test_invalid_address(self):
        reader = geoip2.database.Reader(
            'tests/data/test-data/GeoIP2-City-Test.mmdb')
        with self.assertRaisesRegex(ValueError,
                                    'The value "invalid" is not a valid '
                                    'IP address.'):
            reader.city('invalid')
        reader.close()
