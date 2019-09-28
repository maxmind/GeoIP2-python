"""
Models
======

These classes provide models for the data returned by the GeoIP2
web service and databases.

The only difference between the City and Insights model classes is which
fields in each record may be populated. See
http://dev.maxmind.com/geoip/geoip2/web-services for more details.

"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods
import ipaddress
from abc import ABCMeta

import geoip2.records
from geoip2.compat import compat_ip_network
from geoip2.mixins import SimpleEquality


class Country(SimpleEquality):
    """Model for the GeoIP2 Precision: Country and the GeoIP2 Country database.

    This class provides the following attributes:

    .. attribute:: continent

      Continent object for the requested IP address.

      :type: :py:class:`geoip2.records.Continent`

    .. attribute:: country

      Country object for the requested IP address. This record represents the
      country where MaxMind believes the IP is located.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: maxmind

      Information related to your MaxMind account.

      :type: :py:class:`geoip2.records.MaxMind`

    .. attribute:: registered_country

      The registered country object for the requested IP address. This record
      represents the country where the ISP has registered a given IP block in
      and may differ from the user's country.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: represented_country

      Object for the country represented by the users of the IP address
      when that country is different than the country in ``country``. For
      instance, the country represented by an overseas military base.

      :type: :py:class:`geoip2.records.RepresentedCountry`

    .. attribute:: traits

      Object with the traits of the requested IP address.

      :type: :py:class:`geoip2.records.Traits`

    """
    def __init__(self, raw_response, locales=None):
        if locales is None:
            locales = ['en']
        self._locales = locales
        self.continent = \
            geoip2.records.Continent(locales,
                                     **raw_response.get('continent', {}))
        self.country = \
            geoip2.records.Country(locales,
                                   **raw_response.get('country', {}))
        self.registered_country = \
            geoip2.records.Country(locales,
                                   **raw_response.get('registered_country',
                                                      {}))
        self.represented_country \
            = geoip2.records.RepresentedCountry(locales,
                                                **raw_response.get(
                                                    'represented_country', {}))

        self.maxmind = \
            geoip2.records.MaxMind(**raw_response.get('maxmind', {}))

        self.traits = geoip2.records.Traits(**raw_response.get('traits', {}))
        self.raw = raw_response

    def __repr__(self):
        return '{module}.{class_name}({data}, {locales})'.format(
            module=self.__module__,
            class_name=self.__class__.__name__,
            data=self.raw,
            locales=self._locales)


class City(Country):
    """Model for the GeoIP2 Precision: City and the GeoIP2 City database.

    .. attribute:: city

      City object for the requested IP address.

      :type: :py:class:`geoip2.records.City`

    .. attribute:: continent

      Continent object for the requested IP address.

      :type: :py:class:`geoip2.records.Continent`

    .. attribute:: country

      Country object for the requested IP address. This record represents the
      country where MaxMind believes the IP is located.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: location

      Location object for the requested IP address.

    .. attribute:: maxmind

      Information related to your MaxMind account.

      :type: :py:class:`geoip2.records.MaxMind`

    .. attribute:: registered_country

      The registered country object for the requested IP address. This record
      represents the country where the ISP has registered a given IP block in
      and may differ from the user's country.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: represented_country

      Object for the country represented by the users of the IP address
      when that country is different than the country in ``country``. For
      instance, the country represented by an overseas military base.

      :type: :py:class:`geoip2.records.RepresentedCountry`

    .. attribute:: subdivisions

      Object (tuple) representing the subdivisions of the country to which
      the location of the requested IP address belongs.

      :type: :py:class:`geoip2.records.Subdivisions`

    .. attribute:: traits

      Object with the traits of the requested IP address.

      :type: :py:class:`geoip2.records.Traits`

    """
    def __init__(self, raw_response, locales=None):
        super(City, self).__init__(raw_response, locales)
        self.city = \
            geoip2.records.City(locales, **raw_response.get('city', {}))
        self.location = \
            geoip2.records.Location(**raw_response.get('location', {}))
        self.postal = \
            geoip2.records.Postal(**raw_response.get('postal', {}))
        self.subdivisions = \
            geoip2.records.Subdivisions(locales,
                                        *raw_response.get('subdivisions', []))


class Insights(City):
    """Model for the GeoIP2 Precision: Insights web service endpoint.

    .. attribute:: city

      City object for the requested IP address.

      :type: :py:class:`geoip2.records.City`

    .. attribute:: continent

      Continent object for the requested IP address.

      :type: :py:class:`geoip2.records.Continent`

    .. attribute:: country

      Country object for the requested IP address. This record represents the
      country where MaxMind believes the IP is located.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: location

      Location object for the requested IP address.

    .. attribute:: maxmind

      Information related to your MaxMind account.

      :type: :py:class:`geoip2.records.MaxMind`

    .. attribute:: registered_country

      The registered country object for the requested IP address. This record
      represents the country where the ISP has registered a given IP block in
      and may differ from the user's country.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: represented_country

      Object for the country represented by the users of the IP address
      when that country is different than the country in ``country``. For
      instance, the country represented by an overseas military base.

      :type: :py:class:`geoip2.records.RepresentedCountry`

    .. attribute:: subdivisions

      Object (tuple) representing the subdivisions of the country to which
      the location of the requested IP address belongs.

      :type: :py:class:`geoip2.records.Subdivisions`

    .. attribute:: traits

      Object with the traits of the requested IP address.

      :type: :py:class:`geoip2.records.Traits`

    """


class Enterprise(City):
    """Model for the GeoIP2 Enterprise database.

    .. attribute:: city

      City object for the requested IP address.

      :type: :py:class:`geoip2.records.City`

    .. attribute:: continent

      Continent object for the requested IP address.

      :type: :py:class:`geoip2.records.Continent`

    .. attribute:: country

      Country object for the requested IP address. This record represents the
      country where MaxMind believes the IP is located.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: location

      Location object for the requested IP address.

    .. attribute:: maxmind

      Information related to your MaxMind account.

      :type: :py:class:`geoip2.records.MaxMind`

    .. attribute:: registered_country

      The registered country object for the requested IP address. This record
      represents the country where the ISP has registered a given IP block in
      and may differ from the user's country.

      :type: :py:class:`geoip2.records.Country`

    .. attribute:: represented_country

      Object for the country represented by the users of the IP address
      when that country is different than the country in ``country``. For
      instance, the country represented by an overseas military base.

      :type: :py:class:`geoip2.records.RepresentedCountry`

    .. attribute:: subdivisions

      Object (tuple) representing the subdivisions of the country to which
      the location of the requested IP address belongs.

      :type: :py:class:`geoip2.records.Subdivisions`

    .. attribute:: traits

      Object with the traits of the requested IP address.

      :type: :py:class:`geoip2.records.Traits`

    """


class SimpleModel(SimpleEquality):
    """Provides basic methods for non-location models"""

    __metaclass__ = ABCMeta

    def __init__(self, raw):
        self.raw = raw
        self._network = None
        self._prefix_len = raw.get('prefix_len')
        self.ip_address = raw.get('ip_address')

    def __repr__(self):
        # pylint: disable=no-member
        return '{module}.{class_name}({data})'.format(
            module=self.__module__,
            class_name=self.__class__.__name__,
            data=str(self.raw))

    @property
    def network(self):
        """The network for the record"""
        # This code is duplicated for performance reasons
        # pylint: disable=duplicate-code
        network = self._network
        if isinstance(network, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            return network

        ip_address = self.ip_address
        prefix_len = self._prefix_len
        if ip_address is None or prefix_len is None:
            return None
        network = compat_ip_network("{}/{}".format(ip_address, prefix_len),
                                    False)
        self._network = network
        return network


class AnonymousIP(SimpleModel):
    """Model class for the GeoIP2 Anonymous IP.

    This class provides the following attribute:

    .. attribute:: is_anonymous

      This is true if the IP address belongs to any sort of anonymous network.

      :type: bool

    .. attribute:: is_anonymous_vpn

      This is true if the IP address is registered to an anonymous VPN
      provider.

      If a VPN provider does not register subnets under names associated with
      them, we will likely only flag their IP ranges using the
      ``is_hosting_provider`` attribute.

      :type: bool

    .. attribute:: is_hosting_provider

      This is true if the IP address belongs to a hosting or VPN provider
      (see description of ``is_anonymous_vpn`` attribute).

      :type: bool

    .. attribute:: is_public_proxy

      This is true if the IP address belongs to a public proxy.

      :type: bool

    .. attribute:: is_tor_exit_node

      This is true if the IP address is a Tor exit node.

      :type: bool

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: unicode

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """
    def __init__(self, raw):
        super(AnonymousIP, self).__init__(raw)
        self.is_anonymous = raw.get('is_anonymous', False)
        self.is_anonymous_vpn = raw.get('is_anonymous_vpn', False)
        self.is_hosting_provider = raw.get('is_hosting_provider', False)
        self.is_public_proxy = raw.get('is_public_proxy', False)
        self.is_tor_exit_node = raw.get('is_tor_exit_node', False)


class ASN(SimpleModel):
    """Model class for the GeoLite2 ASN.

    This class provides the following attribute:

    .. attribute:: autonomous_system_number

      The autonomous system number associated with the IP address.

      :type: int

    .. attribute:: autonomous_system_organization

      The organization associated with the registered autonomous system number
      for the IP address.

      :type: unicode

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: unicode

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """

    # pylint:disable=too-many-arguments
    def __init__(self, raw):
        super(ASN, self).__init__(raw)
        self.autonomous_system_number = raw.get('autonomous_system_number')
        self.autonomous_system_organization = raw.get(
            'autonomous_system_organization')


class ConnectionType(SimpleModel):
    """Model class for the GeoIP2 Connection-Type.

    This class provides the following attribute:

    .. attribute:: connection_type

      The connection type may take the following values:

      - Dialup
      - Cable/DSL
      - Corporate
      - Cellular

      Additional values may be added in the future.

      :type: unicode

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: unicode

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """
    def __init__(self, raw):
        super(ConnectionType, self).__init__(raw)
        self.connection_type = raw.get('connection_type')


class Domain(SimpleModel):
    """Model class for the GeoIP2 Domain.

    This class provides the following attribute:

    .. attribute:: domain

      The domain associated with the IP address.

      :type: unicode

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: unicode

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network

    """
    def __init__(self, raw):
        super(Domain, self).__init__(raw)
        self.domain = raw.get('domain')


class ISP(ASN):
    """Model class for the GeoIP2 ISP.

    This class provides the following attribute:

    .. attribute:: autonomous_system_number

      The autonomous system number associated with the IP address.

      :type: int

    .. attribute:: autonomous_system_organization

      The organization associated with the registered autonomous system number
      for the IP address.

      :type: unicode

    .. attribute:: isp

      The name of the ISP associated with the IP address.

      :type: unicode

    .. attribute:: organization

      The name of the organization associated with the IP address.

      :type: unicode

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: unicode

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """

    # pylint:disable=too-many-arguments
    def __init__(self, raw):
        super(ISP, self).__init__(raw)
        self.isp = raw.get('isp')
        self.organization = raw.get('organization')
