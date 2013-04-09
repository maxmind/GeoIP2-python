"""
GeoIP2 WebService Client API
============================

This class provides a client API for all the GeoIP Precision web service's end
points. The end points are Country, City, City/ISP/Org, and Omni. Each end
point returns a different set of data about an IP address, with Country
returning the least data and Omni the most.

Each web service end point is represented by a different model class, and
these model classes in turn contain multiple Record classes. The record
classes have attributes which contain data about the IP address.

If the web service does not return a particular piece of data for an IP
address, the associated attribute is not populated.

The web service may not return any information for an entire record, in which
case all of the attributes for that record class will be empty.

SSL
---

Requests to the GeoIP Precision web service are always made with SSL.

Usage
-----

The basic API for this class is the same for all of the web service end
points. First you create a web service object with your MaxMind C<user_id> and
C<license_key>, then you call the method corresponding to a specific end
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
    >>> print(country.iso_3166_alpha_2)

Exceptions
----------

For details on the possible errors returned by the web service itself, see
http://dev.maxmind.com/geoip/precision for the GeoIP Precision web service
docs.

If the web service returns an explicit error document, this is thrown as a
GeoIP2WebServiceError exception. If some other sort of error occurs, this is
thrown as a GeoIP2HTTPError. The difference is that the webservice error
includes an error message and error code delivered by the web service. The
latter is thrown when some sort of unanticipated error occurs, such as the
web service returning a 500 or an invalid error document.

If the web service returns any status code besides 200, 4xx, or 5xx, this also
becomes a GeoIP2HTTPError.

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

See http://dev.maxmind.com/geoip/precision for details on what data each end
point may return.

The only piece of data which is always returned is the ip_address key in
the geoip.records.Traits record.

Every record class attribute has a corresponding predicate method so you can
check to see if the attribute is set.

"""
import geoip2.models
import requests
from .errors import GeoIP2Error, GeoIP2HTTPError, GeoIP2WebServiceError


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
          passed onto record classes to use when their name properties are
          called. The default value is ['en'].

        Details on language handling:

        The order of the languages is significant. When a record class has
        multiple names (country, city, etc.), its name property will return
        the name in the first language that has one.

        Note that the only language which is always present in the GeoIP2
        Precision data in "en". If you do not include this language, the 
        name property may end up returning None even when the record hass
        an English name.

        Currently, the valid list of language codes is:

        en -- English names may still include accented characters if that is
          the accepted spelling in English. In other words, English does not
          mean ASCII.
        ja -- Japanese
        ru -- Russian
        zh-CN -- Simplified Chinese.

        Passing any other language code will result in an error.

        """

    def __init__(self, user_id, license_key, host='geoip.maxmind.com',
                 languages=None):
        if languages is None:
            languages = ['en']
        self.languages = languages
        self.user_id = user_id
        self.license_key = license_key
        self._base_uri = 'https://%s/geoip' % (host)

    def city(self, ip='me'):
        """This method calls the GeoIP2 Precision City endpoint.

        :param ip:IPv4 or IPv6 address as a string. If no address is provided,
        the address that the web service is called from will be used.
        :returns: geoip2.models.City object

        """
        return self._response_for('city', geoip2.models.City, ip)

    def city_isp_org(self, ip='me'):
        """This method calls the GeoIP2 Precision City/ISP/Org endpoint.

        :param ip: IPv4 or IPv6 address as a string. If no address is provided,
        the address that the web service is called from will be used.
        :returns: geoip2.models.CityISPOrg object

        """
        return self._response_for('city_isp_org', geoip2.models.CityISPOrg, ip)

    def country(self, ip='me'):
        """This method calls the GeoIP2 Country endpoint.

        :param ip: IPv4 or IPv6 address as a string. If no address is provided,
        the address that the web service is called from will be used.
        :returns: geoip2.models.Country object

        """
        return self._response_for('country', geoip2.models.Country, ip)

    def omni(self, ip='me'):
        """This method calls the GeoIP2 Precision Omni endpoint.

        :param ip: IPv4 or IPv6 address as a string. If no address is provided,
        the address that the web service is called from will be used.
        :returns: geoip2.models.Omni object

        """
        return self._response_for('omni', geoip2.models.Omni, ip)

    def _response_for(self, path, model_class, ip):
        uri = '/'.join([self._base_uri, path, ip])
        response = requests.get(uri, auth=(self.user_id, self.license_key),
                                headers={'Accept': 'application/json'})
        if (response.status_code == 200):
            body = self._handle_success(response, uri)
            return model_class(body, languages=self.languages)
        else:
            self._handle_error(response, uri)

    def _handle_success(self, response, uri):
        try:
            return response.json()
        except ValueError as e:
            raise GeoIP2HTTPError('Received a 200 response for %(uri)s'
                                  ' but could not decode the response as '
                                  'JSON: ' % locals() +
                                  ', '.join(e.args), 200, uri)

    def _handle_error(self, response, uri):
        status = response.status_code

        if status >= 400 and status < 499:
            self._handle_4xx_status(response, status, uri)
        elif status >= 500 and status < 599:
            self._handle_5xx_status(response, status, uri)
        else:
            self._handle_non_200_status(response, status, uri)

    def _handle_4xx_status(self, response, status, uri):
        if response.content:
            try:
                body = response.json()
            except ValueError as e:
                raise GeoIP2HTTPError(
                    'Received a %(status)i error for %(uri)s but it did'
                    ' not include the expected JSON body: ' % locals() +
                    ', '.join(e.args), status, uri)
            else:
                if 'code' in body and 'error' in body:
                    raise GeoIP2WebServiceError(body.get('error'),
                                                body.get('code'),
                                                status, uri)
                else:
                    raise GeoIP2HTTPError(
                        'Response contains JSON but it does not specify '
                        'code or error keys', status, uri)
        else:
            raise GeoIP2HTTPError('Received a %(status)i error for %(uri)s '
                                  'with no body.' % locals(), status, uri)

    def _handle_5xx_status(self, response, status, uri):
        raise GeoIP2HTTPError('Received a server error (%(status)i) for '
                              '%(uri)s' % locals(), status, uri)

    def _handle_non_200_status(self, response, status, uri):
        raise GeoIP2HTTPError('Received a very surprising HTTP status '
                              '(%(status)i) for %(uri)s' % locals(), status,
                              uri)
"""

:copyright: (c) 2013 by MaxMind, Inc.
:license: LGPL 2.1 or greater, see LICENSE for more details.

"""
