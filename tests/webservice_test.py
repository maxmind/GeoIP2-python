#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import geoip2
import requests_mock
from geoip2.errors import (AddressNotFoundError, AuthenticationError,
                           GeoIP2Error, HTTPError, InvalidRequestError,
                           OutOfQueriesError, PermissionRequiredError)
from geoip2.webservice import Client

if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

if sys.version_info[0] == 2:
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    unittest.TestCase.assertRegex = unittest.TestCase.assertRegexpMatches


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(42, 'abcdef123456')

    base_uri = 'https://geoip.maxmind.com/geoip/v2.1/'
    country = {
        'continent': {
            'code': 'NA',
            'geoname_id': 42,
            'names': {
                'en': 'North America'
            }
        },
        'country': {
            'geoname_id': 1,
            'iso_code': 'US',
            'names': {
                'en': 'United States of America'
            }
        },
        'maxmind': {
            'queries_remaining': 11
        },
        'registered_country': {
            'geoname_id': 2,
            'is_in_european_union': True,
            'iso_code': 'DE',
            'names': {
                'en': 'Germany'
            }
        },
        'traits': {
            'ip_address': '1.2.3.4'
        },
    }

    def _content_type(self, endpoint):
        return ('application/vnd.maxmind.com-' + endpoint +
                '+json; charset=UTF-8; version=1.0')

    @requests_mock.mock()
    def test_country_ok(self, mock):
        mock.get(
            self.base_uri + 'country/1.2.3.4',
            json=self.country,
            status_code=200,
            headers={'Content-Type': self._content_type('country')})
        country = self.client.country('1.2.3.4')
        self.assertEqual(
            type(country), geoip2.models.Country,
            'return value of client.country')
        self.assertEqual(country.continent.geoname_id, 42,
                         'continent geoname_id is 42')
        self.assertEqual(country.continent.code, 'NA', 'continent code is NA')
        self.assertEqual(country.continent.name, 'North America',
                         'continent name is North America')
        self.assertEqual(country.country.geoname_id, 1,
                         'country geoname_id is 1')
        self.assertIs(country.country.is_in_european_union, False,
                      'country is_in_european_union is False')
        self.assertEqual(country.country.iso_code, 'US',
                         'country iso_code is US')
        self.assertEqual(country.country.names,
                         {'en': 'United States of America'}, 'country names')
        self.assertEqual(country.country.name, 'United States of America',
                         'country name is United States of America')
        self.assertEqual(country.maxmind.queries_remaining, 11,
                         'queries_remaining is 11')
        self.assertIs(country.registered_country.is_in_european_union, True,
                      'registered_country is_in_european_union is True')
        self.assertEqual(country.raw, self.country, 'raw response is correct')

    @requests_mock.mock()
    def test_me(self, mock):
        mock.get(
            self.base_uri + 'country/me',
            json=self.country,
            status_code=200,
            headers={'Content-Type': self._content_type('country')})
        implicit_me = self.client.country()
        self.assertEqual(
            type(implicit_me), geoip2.models.Country,
            'country() returns Country object')
        explicit_me = self.client.country()
        self.assertEqual(
            type(explicit_me), geoip2.models.Country,
            'country(\'me\') returns Country object')

    @requests_mock.mock()
    def test_200_error(self, mock):
        mock.get(
            self.base_uri + 'country/1.1.1.1',
            status_code=200,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(GeoIP2Error,
                                    'could not decode the response as JSON'):
            self.client.country('1.1.1.1')

    def test_bad_ip_address(self):
        with self.assertRaisesRegex(ValueError,
                                    "'1.2.3' does not appear to be an IPv4 "
                                    "or IPv6 address"):
            self.client.country('1.2.3')

    @requests_mock.mock()
    def test_no_body_error(self, mock):
        mock.get(
            self.base_uri + 'country/' + '1.2.3.7',
            text='',
            status_code=400,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(
                HTTPError, 'Received a 400 error for .* with no body'):
            self.client.country('1.2.3.7')

    @requests_mock.mock()
    def test_weird_body_error(self, mock):
        mock.get(
            self.base_uri + 'country/' + '1.2.3.8',
            text='{"wierd": 42}',
            status_code=400,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(HTTPError,
                                    'Response contains JSON but it does not '
                                    'specify code or error keys'):
            self.client.country('1.2.3.8')

    @requests_mock.mock()
    def test_bad_body_error(self, mock):
        mock.get(
            self.base_uri + 'country/' + '1.2.3.9',
            text='bad body',
            status_code=400,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(
                HTTPError, 'it did not include the expected JSON body'):
            self.client.country('1.2.3.9')

    @requests_mock.mock()
    def test_500_error(self, mock):
        mock.get(self.base_uri + 'country/' + '1.2.3.10', status_code=500)
        with self.assertRaisesRegex(HTTPError,
                                    'Received a server error \(500\) for'):
            self.client.country('1.2.3.10')

    @requests_mock.mock()
    def test_300_error(self, mock):
        mock.get(
            self.base_uri + 'country/' + '1.2.3.11',
            status_code=300,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(HTTPError,
                                    'Received a very surprising HTTP status '
                                    '\(300\) for'):

            self.client.country('1.2.3.11')

    @requests_mock.mock()
    def test_ip_address_required(self, mock):
        self._test_error(mock, 400, 'IP_ADDRESS_REQUIRED', InvalidRequestError)

    @requests_mock.mock()
    def test_ip_address_not_found(self, mock):
        self._test_error(mock, 404, 'IP_ADDRESS_NOT_FOUND',
                         AddressNotFoundError)

    @requests_mock.mock()
    def test_ip_address_reserved(self, mock):
        self._test_error(mock, 400, 'IP_ADDRESS_RESERVED',
                         AddressNotFoundError)

    @requests_mock.mock()
    def test_permission_required(self, mock):
        self._test_error(mock, 403, 'PERMISSION_REQUIRED',
                         PermissionRequiredError)

    @requests_mock.mock()
    def test_auth_invalid(self, mock):
        self._test_error(mock, 400, 'AUTHORIZATION_INVALID',
                         AuthenticationError)

    @requests_mock.mock()
    def test_license_key_required(self, mock):
        self._test_error(mock, 401, 'LICENSE_KEY_REQUIRED',
                         AuthenticationError)

    @requests_mock.mock()
    def test_account_id_required(self, mock):
        self._test_error(mock, 401, 'ACCOUNT_ID_REQUIRED', AuthenticationError)

    @requests_mock.mock()
    def test_user_id_required(self, mock):
        self._test_error(mock, 401, 'USER_ID_REQUIRED', AuthenticationError)

    @requests_mock.mock()
    def test_account_id_unkown(self, mock):
        self._test_error(mock, 401, 'ACCOUNT_ID_UNKNOWN', AuthenticationError)

    @requests_mock.mock()
    def test_user_id_unkown(self, mock):
        self._test_error(mock, 401, 'USER_ID_UNKNOWN', AuthenticationError)

    @requests_mock.mock()
    def test_out_of_queries_error(self, mock):
        self._test_error(mock, 402, 'OUT_OF_QUERIES', OutOfQueriesError)

    def _test_error(self, mock, status, error_code, error_class):
        msg = 'Some error message'
        body = {'error': msg, 'code': error_code}
        mock.get(
            self.base_uri + 'country/1.2.3.18',
            json=body,
            status_code=status,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(error_class, msg):
            self.client.country('1.2.3.18')

    @requests_mock.mock()
    def test_unknown_error(self, mock):
        msg = 'Unknown error type'
        ip = '1.2.3.19'
        body = {'error': msg, 'code': 'UNKNOWN_TYPE'}
        mock.get(
            self.base_uri + 'country/' + ip,
            json=body,
            status_code=400,
            headers={'Content-Type': self._content_type('country')})
        with self.assertRaisesRegex(InvalidRequestError, msg):
            self.client.country(ip)

    @requests_mock.mock()
    def test_request(self, mock):
        mock.get(
            self.base_uri + 'country/' + '1.2.3.4',
            json=self.country,
            status_code=200,
            headers={'Content-Type': self._content_type('country')})
        self.client.country('1.2.3.4')
        request = mock.request_history[-1]

        self.assertEqual(request.path, '/geoip/v2.1/country/1.2.3.4',
                         'correct URI is used')
        self.assertEqual(request.headers['Accept'], 'application/json',
                         'correct Accept header')
        self.assertRegex(request.headers['User-Agent'],
                         '^GeoIP2 Python Client v', 'Correct User-Agent')
        self.assertEqual(request.headers['Authorization'],
                         'Basic NDI6YWJjZGVmMTIzNDU2', 'correct auth')

    @requests_mock.mock()
    def test_city_ok(self, mock):
        mock.get(
            self.base_uri + 'city/' + '1.2.3.4',
            json=self.country,
            status_code=200,
            headers={'Content-Type': self._content_type('city')})
        city = self.client.city('1.2.3.4')
        self.assertEqual(
            type(city), geoip2.models.City, 'return value of client.city')

    @requests_mock.mock()
    def test_insights_ok(self, mock):
        mock.get(
            self.base_uri + 'insights/1.2.3.4',
            json=self.country,
            status_code=200,
            headers={'Content-Type': self._content_type('country')})
        insights = self.client.insights('1.2.3.4')
        self.assertEqual(
            type(insights), geoip2.models.Insights,
            'return value of client.insights')

    def test_named_constructor_args(self):
        id = '47'
        key = '1234567890ab'
        for client in (Client(account_id=id, license_key=key),
                       Client(user_id=id, license_key=key)):
            self.assertEqual(client._account_id, id)
            self.assertEqual(client._license_key, key)

    def test_missing_constructor_args(self):
        with self.assertRaises(TypeError):
            Client(license_key='1234567890ab')

        with self.assertRaises(TypeError):
            Client('47')


if __name__ == '__main__':
    unittest.main()
