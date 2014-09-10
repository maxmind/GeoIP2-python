#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httpretty
import httpretty.core
import sys
sys.path.append('..')

import geoip2
import json
import requests
from geoip2.errors import AddressNotFoundError, AuthenticationError, \
    GeoIP2Error, HTTPError, InvalidRequestError, OutOfQueriesError
from geoip2.webservice import Client

if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

if sys.version_info[0] == 2:
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    unittest.TestCase.assertRegex = unittest.TestCase.assertRegexpMatches


@httpretty.activate
class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(42, 'abcdef123456',)

    base_uri = 'https://geoip.maxmind.com/geoip/v2.1/'
    country = {
        'continent': {
            'code': 'NA',
            'geoname_id': 42,
            'names': {'en': 'North America'}
        },
        'country': {
            'geoname_id': 1,
            'iso_code': 'US',
            'names': {'en': 'United States of America'}
        },
        'maxmind': {'queries_remaining': 11},
        'traits': {'ip_address': '1.2.3.4'},
    }

    def _content_type(self, endpoint):
        return ('application/vnd.maxmind.com-' +
                endpoint + '+json; charset=UTF-8; version=1.0')

    def test_country_ok(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/1.2.3.4',
                               body=json.dumps(self.country),
                               status=200,
                               content_type=self._content_type('country'))
        country = self.client.country('1.2.3.4')
        self.assertEqual(type(country), geoip2.models.Country,
                         'return value of client.country')
        self.assertEqual(country.continent.geoname_id, 42,
                         'continent geoname_id is 42')
        self.assertEqual(country.continent.code, 'NA',
                         'continent code is NA')
        self.assertEqual(country.continent.name, 'North America',
                         'continent name is North America')
        self.assertEqual(country.country.geoname_id, 1,
                         'country geoname_id is 1')
        self.assertEqual(country.country.iso_code, 'US',
                         'country iso_code is US')
        self.assertEqual(country.country.names,
                         {'en': 'United States of America'},
                         'country names')
        self.assertEqual(country.country.name, 'United States of America',
                         'country name is United States of America')
        self.assertEqual(country.maxmind.queries_remaining, 11,
                         'queries_remaining is 11')
        self.assertEqual(country.raw, self.country, 'raw response is correct')

    def test_me(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/me',
                               body=json.dumps(self.country),
                               status=200,
                               content_type=self._content_type('country'))
        implicit_me = self.client.country()
        self.assertEqual(type(implicit_me), geoip2.models.Country,
                         'country() returns Country object')
        explicit_me = self.client.country()
        self.assertEqual(type(explicit_me), geoip2.models.Country,
                         'country(\'me\') returns Country object')

    def test_200_error(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/1.1.1.1',
                               status=200,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(GeoIP2Error,
                                    'could not decode the response as JSON'):
            self.client.country('1.1.1.1')

    def test_bad_ip_address(self):
        with self.assertRaisesRegex(ValueError,
                                    "'1.2.3' does not appear to be an IPv4 "
                                    "or IPv6 address"):
            self.client.country('1.2.3')

    def test_no_body_error(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.7',
                               body='',
                               status=400,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(HTTPError,
                                    'Received a 400 error for .* with no body'):
            self.client.country('1.2.3.7')

    def test_weird_body_error(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.8',
                               body='{"wierd": 42}',
                               status=400,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(HTTPError,
                                    'Response contains JSON but it does not '
                                    'specify code or error keys'):
            self.client.country('1.2.3.8')

    def test_bad_body_error(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.9',
                               body='bad body',
                               status=400,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(HTTPError,
                                    'it did not include the expected JSON body'
                                    ):
            self.client.country('1.2.3.9')

    def test_500_error(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.10',
                               status=500)
        with self.assertRaisesRegex(HTTPError,
                                    'Received a server error \(500\) for'):
            self.client.country('1.2.3.10')

    def test_300_error(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.11',
                               status=300,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(HTTPError,
                                    'Received a very surprising HTTP status '
                                    '\(300\) for'):

            self.client.country('1.2.3.11')

    def test_address_not_found_error(self):
        body = {'error': 'Not in DB', 'code': 'IP_ADDRESS_NOT_FOUND'}
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.13',
                               body=json.dumps(body),
                               status=404,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(AddressNotFoundError,
                                    'Not in DB'):
            self.client.country('1.2.3.13')

    def test_private_address_error(self):
        body = {'error': 'Private', 'code': 'IP_ADDRESS_RESERVED'}
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.14',
                               body=json.dumps(body),
                               status=401,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(AddressNotFoundError, 'Private'):
            self.client.country('1.2.3.14')

    def test_auth_invalid(self):
        body = {'error': 'Invalid auth', 'code': 'AUTHORIZATION_INVALID'}
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.15',
                               body=json.dumps(body),
                               status=400,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(AuthenticationError, 'Invalid auth'):
            self.client.country('1.2.3.15')

    def test_license_required(self):
        body = {'error': 'License required', 'code': 'LICENSE_KEY_REQUIRED'}
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.16',
                               body=json.dumps(body),
                               status=401,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(AuthenticationError, 'License required'):
            self.client.country('1.2.3.16')

    def test_user_id_required(self):
        body = {'error': 'User ID required', 'code': 'USER_ID_REQUIRED'}
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.17',
                               body=json.dumps(body),
                               status=401,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(AuthenticationError, 'User ID required'):
            self.client.country('1.2.3.17')

    def test_out_of_queries_error(self):
        body = {'error': 'Out of Queries', 'code': 'OUT_OF_QUERIES'}
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.18',
                               body=json.dumps(body),
                               status=402,
                               content_type=self._content_type('country'))
        with self.assertRaisesRegex(OutOfQueriesError, 'Out of Queries',):
            self.client.country('1.2.3.18')

    def test_request(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'country/' + '1.2.3.4',
                               body=json.dumps(self.country),
                               status=200,
                               content_type=self._content_type('country'))
        country = self.client.country('1.2.3.4')
        request = httpretty.core.httpretty.latest_requests[-1]

        self.assertEqual(request.path,
                         '/geoip/v2.1/country/1.2.3.4',
                         'correct URI is used')
        self.assertEqual(request.headers['Accept'],
                         'application/json',
                         'correct Accept header')
        self.assertRegex(request.headers['User-Agent'],
                         '^GeoIP2 Python Client v',
                         'Correct User-Agent')
        self.assertEqual(request.headers['Authorization'],
                         'Basic NDI6YWJjZGVmMTIzNDU2', 'correct auth')

    def test_city_ok(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'city/' + '1.2.3.4',
                               body=json.dumps(self.country),
                               status=200,
                               content_type=self._content_type('city'))
        city = self.client.city('1.2.3.4')
        self.assertEqual(type(city), geoip2.models.City,
                         'return value of client.city')

    def test_insights_ok(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'insights/1.2.3.4',
                               body=json.dumps(self.country),
                               status=200,
                               content_type=self._content_type('country'))
        insights = self.client.insights('1.2.3.4')
        self.assertEqual(type(insights), geoip2.models.Insights,
                         'return value of client.insights')

    def test_insights_ok(self):
        httpretty.register_uri(httpretty.GET,
                               self.base_uri + 'insights/1.2.3.4',
                               body=json.dumps(self.country),
                               status=200,
                               content_type=self._content_type('country'))
        insights = self.client.insights('1.2.3.4')
        self.assertEqual(type(insights), geoip2.models.Insights,
                         'return value of client.insights')

if __name__ == '__main__':
    unittest.main()
