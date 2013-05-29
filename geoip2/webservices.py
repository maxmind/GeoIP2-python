"""
============================
WebServices Client API
============================

This class provides a client API for all the GeoIP2 web service's end
points. The end points are Country, City, City/ISP/Org, and Omni. Each end
point returns a different set of data about an IP address, with Country
returning the least data and Omni the most.

Each web service end point is represented by a different model class, and
these model classes in turn contain multiple record classes. The record
classes have attributes which contain data about the IP address.

If the web service does not return a particular piece of data for an IP
address, the associated attribute is not populated.

The web service may not return any information for an entire record, in which
case all of the attributes for that record class will be empty.

SSL
---

Requests to the GeoIP2 web service are always made with SSL.

Usage
-----

The basic API for this class is the same for all of the web service end
points. First you create a web service object with your MaxMind ``user_id``
and ``license_key``, then you call the method corresponding to a specific end
point, passing it the IP address you want to look up.

If the request succeeds, the method call will return a model class for the end
point you called. This model in turn contains multiple record classes, each of
which represents part of the data returned by the web service.

If the request fails, the client class throws an exception.

Requirements
------------

This library works on Python 2.6+ and Python 3. It requires that the requests
HTTP library is installed. See <http://python-requests.org> for details.

Example
-------

    >>> import geoip2.webservices
    >>> client = geoip2.webservices.Client(42, 'abcdef123456')
    >>> omni = client.omni('24.24.24.24')
    >>> country = omni.country
    >>> print(country.iso_code)

Exceptions
----------

For details on the possible errors returned by the web service itself, see
http://dev.maxmind.com/geoip/geoip2/web-services for the GeoIP2 web service
docs.

If the web service returns an explicit error document, this is thrown as a
WebServiceError exception. If some other sort of error occurs, this is
thrown as an HTTPError. The difference is that the WebServiceError
includes an error message and error code delivered by the web service. The
latter is thrown when some sort of unanticipated error occurs, such as the
web service returning a 500 or an invalid error document.

If the web service returns any status code besides 200, 4xx, or 5xx, this also
becomes an HTTPError.

Finally, if the web service returns a 200 but the body is invalid, the client
throws a GeoIP2Error object.

What data is returned?
----------------------

While many of the end points return the same basic records, the attributes
which can be populated vary between end points. In addition, while an end
point may offer a particular piece of data, MaxMind does not always have every
piece of data for any given IP address.

Because of these factors, it is possible for any end point to return a record
where some or all of the attributes are unpopulated.

See http://dev.maxmind.com/geoip/geoip2/web-services for details on what
data each end point may return.

The only piece of data which is always returned is the :py:attr:`ip_address`
attribute in the :py:class:`geoip2.records.Traits` record.

Every record class attribute has a corresponding predicate method so you can
check to see if the attribute is set.

"""

import geoip2
import geoip2.models
import requests
from requests.utils import default_user_agent
from .errors import GeoIP2Error, HTTPError, WebServiceError

import sys

if sys.version_info[0] == 2 or (sys.version_info[0] == 3
                                and sys.version_info[1] < 3):
    import ipaddr as ipaddress #pylint:disable=F0401
    ipaddress.ip_address = ipaddress.IPAddress
else:
    import ipaddress #pylint:disable=F0401

class Client(object):
    """This method creates a new client object.

    It accepts the following required arguments:

    :param user_id: Your MaxMind User ID.
    :param license_key: Your MaxMind license key.

    Go to https://www.maxmind.com/en/my_license_key to see your MaxMind
    User ID and license key.

    The following keyword arguments are also accepted:

    :param host: The hostname to make a request against. This defaults to
      "geoip.maxmind.com". In most cases, you should not need to set this
      explicitly.
    :param languages: This is list of language codes. This argument will be
      passed on to record classes to use when their name properties are
      called. The default value is ['en'].

      The order of the languages is significant. When a record class has
      multiple names (country, city, etc.), its name property will return
      the name in the first language that has one.

      Note that the only language which is always present in the GeoIP2
      data is "en". If you do not include this language, the name property
      may end up returning None even when the record has an English name.

      Currently, the valid language codes are:

      * de -- German
      * en -- English names may still include accented characters if that is
        the accepted spelling in English. In other words, English does not
        mean ASCII.
      * es -- Spanish
      * fr -- French
      * ja -- Japanese
      * pt-BR -- Brazilian Portuguese
      * ru -- Russian
      * zh-CN -- Simplified Chinese.

    """

    def __init__(self, user_id, license_key, host='geoip.maxmind.com',
                 languages=None):
        if languages is None:
            languages = ['en']
        self.languages = languages
        self.user_id = user_id
        self.license_key = license_key
        self._base_uri = 'https://%s/geoip/v2.0' % (host)

    def city(self, ip_address='me'):
        """This method calls the GeoIP2 Precision City endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no
           address is provided, the address that the web service is
           called from will be used.

        :returns: :py:class:`geoip2.models.City` object

        """
        return self._response_for('city', geoip2.models.City, ip_address)

    def city_isp_org(self, ip_address='me'):
        """This method calls the GeoIP2 Precision City/ISP/Org endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no
          address is provided, the address that the web service is called
          from will be used.

        :returns: :py:class:`geoip2.models.CityISPOrg` object

        """
        return self._response_for('city_isp_org', geoip2.models.CityISPOrg,
                                  ip_address)

    def country(self, ip_address='me'):
        """This method calls the GeoIP2 Country endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Country` object

        """
        return self._response_for('country', geoip2.models.Country,
                                  ip_address)

    def omni(self, ip_address='me'):
        """This method calls the GeoIP2 Precision Omni endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Omni` object

        """
        return self._response_for('omni', geoip2.models.Omni, ip_address)

    def _response_for(self, path, model_class, ip_address):
        if ip_address != 'me':
            ip_address = str(ipaddress.ip_address(ip_address))
        uri = '/'.join([self._base_uri, path, ip_address])
        response = requests.get(uri, auth=(self.user_id, self.license_key),
                                headers={'Accept': 'application/json',
                                         'User-Agent': self._user_agent()})
        if (response.status_code == 200):  #pylint:disable=E1103
            body = self._handle_success(response, uri)
            return model_class(body, languages=self.languages)
        else:
            self._handle_error(response, uri)

    def _user_agent(self):
        return 'GeoIP2 Python Client v%s (%s)' % (geoip2.__version__,
                                                  default_user_agent())

    def _handle_success(self, response, uri):
        try:
            return response.json()
        except ValueError as ex:
            raise GeoIP2Error('Received a 200 response for %(uri)s'
                              ' but could not decode the response as '
                              'JSON: ' % locals() +
                              ', '.join(ex.args), 200, uri)

    def _handle_error(self, response, uri):
        status = response.status_code

        if status >= 400 and status < 499:
            self._handle_4xx_status(response, status, uri)
        elif status >= 500 and status < 599:
            self._handle_5xx_status(status, uri)
        else:
            self._handle_non_200_status(status, uri)

    def _handle_4xx_status(self, response, status, uri):
        if response.content and \
                response.headers['Content-Type'].find('json') >= 0:
            try:
                body = response.json()
            except ValueError as ex:
                raise HTTPError(
                    'Received a %(status)i error for %(uri)s but it did'
                    ' not include the expected JSON body: ' % locals() +
                    ', '.join(ex.args), status, uri)
            else:
                if 'code' in body and 'error' in body:
                    raise WebServiceError(body.get('error'),
                                          body.get('code'),
                                          status, uri)
                else:
                    raise HTTPError(
                        'Response contains JSON but it does not specify '
                        'code or error keys', status, uri)
        elif response.content:
            raise HTTPError('Received a %i for %s with the following '
                            'body: %s' %
                            (status, uri, response.content),
                            status, uri)
        else:
            raise HTTPError('Received a %(status)i error for %(uri)s '
                            'with no body.' % locals(), status, uri)

    def _handle_5xx_status(self, status, uri):
        raise HTTPError('Received a server error (%(status)i) for '
                        '%(uri)s' % locals(), status, uri)

    def _handle_non_200_status(self, status, uri):
        raise HTTPError('Received a very surprising HTTP status '
                        '(%(status)i) for %(uri)s' % locals(), status,
                        uri)
"""

:copyright: (c) 2013 by MaxMind, Inc.
:license: GNU Lesser General Public License v2 or later (LGPLv2+)

"""
