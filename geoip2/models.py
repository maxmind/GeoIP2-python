"""
Models
======

These classes provide models for the data returned by the GeoIP2
web service and databases.

The only difference between the City and Insights model classes is which
fields in each record may be populated. See
https://dev.maxmind.com/geoip/docs/web-services?lang=en for more details.

"""

# pylint: disable=too-many-instance-attributes,too-few-public-methods,too-many-arguments
import ipaddress
from abc import ABCMeta
from collections.abc import Sequence
from typing import Optional, Union
from ipaddress import IPv4Address, IPv6Address

import geoip2.records
from geoip2._internal import Model
from geoip2.types import IPAddress


class Country(Model):
    """Model for the Country web service and Country database.

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

    continent: geoip2.records.Continent
    country: geoip2.records.Country
    maxmind: geoip2.records.MaxMind
    registered_country: geoip2.records.Country
    represented_country: geoip2.records.RepresentedCountry
    traits: geoip2.records.Traits

    def __init__(
        self,
        locales: Optional[Sequence[str]],
        *,
        continent: Optional[dict] = None,
        country: Optional[dict] = None,
        ip_address: Optional[IPAddress] = None,
        maxmind: Optional[dict] = None,
        prefix_len: Optional[int] = None,
        registered_country: Optional[dict] = None,
        represented_country: Optional[dict] = None,
        traits: Optional[dict] = None,
        **_,
    ) -> None:
        self._locales = locales
        self.continent = geoip2.records.Continent(locales, **(continent or {}))
        self.country = geoip2.records.Country(locales, **(country or {}))
        self.registered_country = geoip2.records.Country(
            locales,
            **(registered_country or {}),
        )
        self.represented_country = geoip2.records.RepresentedCountry(
            locales,
            **(represented_country or {}),
        )

        self.maxmind = geoip2.records.MaxMind(**(maxmind or {}))

        traits = traits or {}
        if ip_address is not None:
            traits["ip_address"] = ip_address
        if prefix_len is not None:
            traits["prefix_len"] = prefix_len

        self.traits = geoip2.records.Traits(**traits)

    def __repr__(self) -> str:
        return (
            f"{self.__module__}.{self.__class__.__name__}({self._locales!r}, "
            f"{', '.join(f'{k}={v!r}' for k, v in self.to_dict().items())})"
        )


class City(Country):
    """Model for the City Plus web service and the City database.

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

      :type: :py:class:`geoip2.records.Location`

    .. attribute:: maxmind

      Information related to your MaxMind account.

      :type: :py:class:`geoip2.records.MaxMind`

    .. attribute:: postal

      Postal object for the requested IP address.

      :type: :py:class:`geoip2.records.Postal`

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

    city: geoip2.records.City
    location: geoip2.records.Location
    postal: geoip2.records.Postal
    subdivisions: geoip2.records.Subdivisions

    def __init__(
        self,
        locales: Optional[Sequence[str]],
        *,
        city: Optional[dict] = None,
        continent: Optional[dict] = None,
        country: Optional[dict] = None,
        location: Optional[dict] = None,
        ip_address: Optional[IPAddress] = None,
        maxmind: Optional[dict] = None,
        postal: Optional[dict] = None,
        prefix_len: Optional[int] = None,
        registered_country: Optional[dict] = None,
        represented_country: Optional[dict] = None,
        subdivisions: Optional[list[dict]] = None,
        traits: Optional[dict] = None,
        **_,
    ) -> None:
        super().__init__(
            locales,
            continent=continent,
            country=country,
            ip_address=ip_address,
            maxmind=maxmind,
            prefix_len=prefix_len,
            registered_country=registered_country,
            represented_country=represented_country,
            traits=traits,
        )
        self.city = geoip2.records.City(locales, **(city or {}))
        self.location = geoip2.records.Location(**(location or {}))
        self.postal = geoip2.records.Postal(**(postal or {}))
        self.subdivisions = geoip2.records.Subdivisions(locales, *(subdivisions or []))


class Insights(City):
    """Model for the GeoIP2 Insights web service.

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


class SimpleModel(Model, metaclass=ABCMeta):
    """Provides basic methods for non-location models."""

    _ip_address: IPAddress
    _network: Optional[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]
    _prefix_len: Optional[int]

    def __init__(
        self,
        ip_address: IPAddress,
        network: Optional[str],
        prefix_len: Optional[int],
    ) -> None:
        if network:
            self._network = ipaddress.ip_network(network, False)
            self._prefix_len = self._network.prefixlen
        else:
            # This case is for MMDB lookups where performance is paramount.
            # This is why we don't generate the network unless .network is
            # used.
            self._network = None
            self._prefix_len = prefix_len
        self._ip_address = ip_address

    def __repr__(self) -> str:
        d = self.to_dict()
        d.pop("ip_address", None)
        return (
            f"{self.__module__}.{self.__class__.__name__}("
            + repr(str(self._ip_address))
            + ", "
            + ", ".join(f"{k}={v!r}" for k, v in d.items())
            + ")"
        )

    @property
    def ip_address(self) -> Union[IPv4Address, IPv6Address]:
        """The IP address for the record."""
        if not isinstance(self._ip_address, (IPv4Address, IPv6Address)):
            self._ip_address = ipaddress.ip_address(self._ip_address)
        return self._ip_address

    @property
    def network(self) -> Optional[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]:
        """The network for the record."""
        # This code is duplicated for performance reasons
        network = self._network
        if network is not None:
            return network

        ip_address = self.ip_address
        prefix_len = self._prefix_len
        if ip_address is None or prefix_len is None:
            return None
        network = ipaddress.ip_network(f"{ip_address}/{prefix_len}", False)
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

    .. attribute:: is_residential_proxy

      This is true if the IP address is on a suspected anonymizing network
      and belongs to a residential ISP.

      :type: bool

    .. attribute:: is_tor_exit_node

      This is true if the IP address is a Tor exit node.

      :type: bool

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: ipaddress.IPv4Address or ipaddress.IPv6Address

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """

    is_anonymous: bool
    is_anonymous_vpn: bool
    is_hosting_provider: bool
    is_public_proxy: bool
    is_residential_proxy: bool
    is_tor_exit_node: bool

    def __init__(
        self,
        ip_address: IPAddress,
        *,
        is_anonymous: bool = False,
        is_anonymous_vpn: bool = False,
        is_hosting_provider: bool = False,
        is_public_proxy: bool = False,
        is_residential_proxy: bool = False,
        is_tor_exit_node: bool = False,
        network: Optional[str] = None,
        prefix_len: Optional[int] = None,
        **_,
    ) -> None:
        super().__init__(ip_address, network, prefix_len)
        self.is_anonymous = is_anonymous
        self.is_anonymous_vpn = is_anonymous_vpn
        self.is_hosting_provider = is_hosting_provider
        self.is_public_proxy = is_public_proxy
        self.is_residential_proxy = is_residential_proxy
        self.is_tor_exit_node = is_tor_exit_node


class ASN(SimpleModel):
    """Model class for the GeoLite2 ASN.

    This class provides the following attribute:

    .. attribute:: autonomous_system_number

      The autonomous system number associated with the IP address.

      :type: int

    .. attribute:: autonomous_system_organization

      The organization associated with the registered autonomous system number
      for the IP address.

      :type: str

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: ipaddress.IPv4Address or ipaddress.IPv6Address

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """

    autonomous_system_number: Optional[int]
    autonomous_system_organization: Optional[str]

    # pylint:disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        ip_address: IPAddress,
        *,
        autonomous_system_number: Optional[int] = None,
        autonomous_system_organization: Optional[str] = None,
        network: Optional[str] = None,
        prefix_len: Optional[int] = None,
        **_,
    ) -> None:
        super().__init__(ip_address, network, prefix_len)
        self.autonomous_system_number = autonomous_system_number
        self.autonomous_system_organization = autonomous_system_organization


class ConnectionType(SimpleModel):
    """Model class for the GeoIP2 Connection-Type.

    This class provides the following attribute:

    .. attribute:: connection_type

      The connection type may take the following values:

      - Dialup
      - Cable/DSL
      - Corporate
      - Cellular
      - Satellite

      Additional values may be added in the future.

      :type: str

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: ipaddress.IPv4Address or ipaddress.IPv6Address

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """

    connection_type: Optional[str]

    def __init__(
        self,
        ip_address: IPAddress,
        *,
        connection_type: Optional[str] = None,
        network: Optional[str] = None,
        prefix_len: Optional[int] = None,
        **_,
    ) -> None:
        super().__init__(ip_address, network, prefix_len)
        self.connection_type = connection_type


class Domain(SimpleModel):
    """Model class for the GeoIP2 Domain.

    This class provides the following attribute:

    .. attribute:: domain

      The domain associated with the IP address.

      :type: str

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: ipaddress.IPv4Address or ipaddress.IPv6Address

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network

    """

    domain: Optional[str]

    def __init__(
        self,
        ip_address: IPAddress,
        *,
        domain: Optional[str] = None,
        network: Optional[str] = None,
        prefix_len: Optional[int] = None,
        **_,
    ) -> None:
        super().__init__(ip_address, network, prefix_len)
        self.domain = domain


class ISP(ASN):
    """Model class for the GeoIP2 ISP.

    This class provides the following attribute:

    .. attribute:: autonomous_system_number

      The autonomous system number associated with the IP address.

      :type: int

    .. attribute:: autonomous_system_organization

      The organization associated with the registered autonomous system number
      for the IP address.

      :type: str

    .. attribute:: isp

      The name of the ISP associated with the IP address.

      :type: str

    .. attribute: mobile_country_code

      The `mobile country code (MCC)
      <https://en.wikipedia.org/wiki/Mobile_country_code>`_ associated with the
      IP address and ISP.

      :type: str

    .. attribute: mobile_network_code

      The `mobile network code (MNC)
      <https://en.wikipedia.org/wiki/Mobile_country_code>`_ associated with the
      IP address and ISP.

      :type: str

    .. attribute:: organization

      The name of the organization associated with the IP address.

      :type: str

    .. attribute:: ip_address

      The IP address used in the lookup.

      :type: ipaddress.IPv4Address or ipaddress.IPv6Address

    .. attribute:: network

      The network associated with the record. In particular, this is the
      largest network where all of the fields besides ip_address have the same
      value.

      :type: ipaddress.IPv4Network or ipaddress.IPv6Network
    """

    isp: Optional[str]
    mobile_country_code: Optional[str]
    mobile_network_code: Optional[str]
    organization: Optional[str]

    # pylint:disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        ip_address: IPAddress,
        *,
        autonomous_system_number: Optional[int] = None,
        autonomous_system_organization: Optional[str] = None,
        isp: Optional[str] = None,
        mobile_country_code: Optional[str] = None,
        mobile_network_code: Optional[str] = None,
        organization: Optional[str] = None,
        network: Optional[str] = None,
        prefix_len: Optional[int] = None,
        **_,
    ) -> None:
        super().__init__(
            autonomous_system_number=autonomous_system_number,
            autonomous_system_organization=autonomous_system_organization,
            ip_address=ip_address,
            network=network,
            prefix_len=prefix_len,
        )
        self.isp = isp
        self.mobile_country_code = mobile_country_code
        self.mobile_network_code = mobile_network_code
        self.organization = organization
