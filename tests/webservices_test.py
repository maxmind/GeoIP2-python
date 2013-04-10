#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
sys.path.append('..')

import geoip2
import json
import requests
from geoip2.errors import GeoIP2Error, GeoIP2HTTPError, GeoIP2WebServiceError
from geoip2.webservices import Client

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


@patch.object(requests, 'get')
class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(42, 'abcdef123456',)

    country = {
        'continent': {
            'continent_code': 'NA',
            'geoname_id': 42,
            'name': { 'en': 'North America' }
            },
        'country': {
            'geoname_id': 1,
            'iso_3166_1_alpha_2': 'US',
            'iso_3166_1_alpha_3': 'USA',
            'name': { 'en': 'United States of America'}
            },
        'traits': {'ip_address': '1.2.3.4',},
        }

    def _setup_get(self, get, endpoint='country', status=200, body=None,
                   raw_body=None):
        if body and raw_body:
            raise ValueError('Both body and raw_body cannot be set')
        r = requests.Response()
        r.status_code = status
        if status == 200 or ( status >= 400 and status < 500 ):
            r.headers = {'content-type': ('application/vnd.maxmind.com-%s+'
                                          'json; charset=UTF-8; version=1.0'
                                          % (endpoint,))}
        # Monkey-patching .json. A bit ugly.
        func_type = type(r.json)
        if body:
            # XXX - ugly.
            r._content = json.dumps(body)
            r.json = func_type(lambda x: body, r)
        else:
            if raw_body:
                r._content = raw_body
            def raise_exception(*args):
                raise ValueError('test')
            r.json = func_type(raise_exception, r)

        get.return_value = r

    def test_country_ok(self, get):
        self._setup_get(get, 'country', 200, self.country)
        country = self.client.country('1.2.3.4')
        self.assertEqual(type(country), geoip2.models.Country,
                          'return value of client.country')
        self.assertEqual(country.continent.geoname_id, 42,
                         'continent geoname_id is 42')
        self.assertEqual(country.continent.continent_code, 'NA',
                         'continent continent_code is NA')
        self.assertEqual(country.continent.name, 'North America',
                         'continent name is North America')
        self.assertEqual(country.country.geoname_id, 1,
                         'country geoname_id is 1')
        self.assertEqual(country.country.iso_3166_1_alpha_2, 'US',
                         'country iso_3166_1_alpha_2 is US')
        self.assertEqual(country.country.iso_3166_1_alpha_3, 'USA',
                         'country iso_3166_1_alpha_3 is USA')
        self.assertEqual(country.country.names,
                         { 'en': 'United States of America' },
                         'country names' )
        self.assertEqual(country.country.name, 'United States of America',
                         'country name is United States of America')
        self.assertEqual(country.raw, self.country, 'raw response is correct')

    def test_me(self, get):
        self._setup_get(get, body=self.country)
        implicit_me = self.client.country()
        self.assertEqual(type(implicit_me), geoip2.models.Country,
                          'country() returns Country object')
        explicit_me = self.client.country()
        self.assertEqual(type(explicit_me), geoip2.models.Country,
                          'country(\'me\') returns Country object')

    def test_200_error(self, get):
        self._setup_get(get)
        with self.assertRaisesRegex(GeoIP2Error,
                                     'could not decode the response as JSON'):
            self.client.country('1.1.1.1')

    def test_400_error(self, get):
        body = {'code': 'IP_ADDRESS_INVALID',
                'error': 'The value "1.2.3" is not a '
                'valid ip address',}
        self._setup_get(get, status=400, body=body)
        with self.assertRaisesRegex(GeoIP2WebServiceError,
                                     'The value "1.2.3" is not a valid '
                                    'ip address'):
            self.client.country('1.2.3')
        # XXX - there might be a better way to do this
        try:
            self.client.country('1.2.3')
        except GeoIP2WebServiceError as e:
            self.assertEqual(e.http_status, 400,
                             'exception object contains expected http_status'
                             )
            self.assertEqual(e.code,'IP_ADDRESS_INVALID',
                             'exception object contains expected code'
                             )

    def test_no_body_error(self, get):
        self._setup_get(get, status=400)
        with self.assertRaisesRegex(GeoIP2HTTPError,
                                    'Received a 400 error for .* with no body'):
            self.client.country('1.2.3.7')
        
    def test_weird_body_error(self, get):
        self._setup_get(get, status=400, body={ 'weird': 42 },)
        with self.assertRaisesRegex(GeoIP2HTTPError,
                                    'Response contains JSON but it does not '
                                    'specify code or error keys'):
            self.client.country('1.2.3.8')

    def test_bad_body_error(self, get):
        self._setup_get(get, status=400, raw_body='bad body')
        with self.assertRaisesRegex(GeoIP2HTTPError,
                                    'it did not include the expected JSON body'
                                    ):
            self.client.country('1.2.3.9')

    def test_500_error(self, get):
        self._setup_get(get, status=500)
        with self.assertRaisesRegex(GeoIP2HTTPError,
                                    'Received a server error \(500\) for'):
            self.client.country('1.2.3.10')

    def test_300_error(self, get):
        self._setup_get(get, status=300)
        with self.assertRaisesRegex(GeoIP2HTTPError,
                                    'Received a very surprising HTTP status '
                                    '\(300\) for'):

            self.client.country('1.2.3.11')

    def test_request(self, get):
        self._setup_get(get, 'country', 200, self.country)
        country = self.client.country('1.2.3.4')
        get.assert_called_with('https://geoip.maxmind.com'
                               '/geoip/country/1.2.3.4',
                               headers={'Accept': 'application/json'},
                               auth=(42, 'abcdef123456'))

    def test_city_ok(self, get):
        self._setup_get(get, 'city', 200, self.country)
        city = self.client.city('1.2.3.4')
        self.assertEqual(type(city), geoip2.models.City,
                          'return value of client.city')

    def test_city_isp_org_ok(self, get):
        self._setup_get(get, 'city_isp_org', 200, self.country)
        city_isp_org = self.client.city_isp_org('1.2.3.4')
        self.assertEqual(type(city_isp_org), geoip2.models.CityISPOrg,
                          'return value of client.city_isp_org')

    def test_omni_ok(self, get):
        self._setup_get(get, 'omni', 200, self.country)
        omni = self.client.omni('1.2.3.4')
        self.assertEqual(type(omni), geoip2.models.Omni,
                          'return value of client.omni')

if __name__ == '__main__':
    unittest.main()
