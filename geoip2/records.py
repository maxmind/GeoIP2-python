"""
Records
=======
"""
from abc import ABCMeta


class Record(object):
    """All records are subclasses of ``Record``"""
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        valid_args = dict((k, kwargs.get(k)) for k in self._valid_attributes)
        self.__dict__.update(valid_args)

    def __setattr__(self, name, value):
        raise NotImplementedError(name + ' is read-only.')


class PlaceRecord(Record):
    """All records with :py:attr:`names` subclass :py:class:`PlaceRecord`"""
    __metaclass__ = ABCMeta

    def __init__(self, languages=None, **kwargs):
        if languages is None:
            languages = []
        object.__setattr__(self, 'languages', languages)
        super(PlaceRecord, self).__init__(**kwargs)

    @property
    def name(self):
        return next((self.names.get(x) for x in self.languages if x in
                     self.names), None)


class City(PlaceRecord):
    """Contains data for the city record associated with an IP address

    This class contains the city-level data associated with an IP address.

    This record is returned by all the end points except the Country end point.

    Attributes:

    :ivar confidence: This returns a value from 0-100 indicating MaxMind's
      confidence that the city is correct. This attribute is only available
      from the Omni end point.
    :ivar geoname_id: This returns a GeoName ID for the city. This attribute
      is returned by all end points.
    :ivar name: Returns the name of the city based on the languages list
      passed to the constructor. This attribute is returned by all end points.
    :ivar names: This returns a dictionary where the keys are language codes
      and the values are names. This attribute is returned by all end points.

    """
    _valid_attributes = set(['confidence', 'geoname_id', 'names'])


class Continent(PlaceRecord):
    """Contains data for the continent record associated with an IP address

    This class contains the continent-level data associated with an IP
    address.

    This record is returned by all the end points.

    Attributes:

    :ivar continent_code:  This returns a two character continent code
      like "NA" (North America) or "OC" (Oceania). This attribute is returned
      by all end points.
    :ivar geoname_id: This returns a GeoName ID for the continent. This
      attribute is returned by all end points.
    :ivar name: Returns the name of the continent based on the languages list
      passed to the constructor. This attribute is returned by all end points.
    :ivar names: This returns a dictionary where the keys are language codes
      and the values are names. This attribute is returned by all end points.

    """
    _valid_attributes = set(['continent_code', 'geoname_id', 'names'])


class Country(PlaceRecord):
    """Contains data for the country record associated with an IP address

    This class contains the country-level data associated with an IP address.

    This record is returned by all the end points except the Country end point.

    Attributes:

    :ivar confidence: This returns a value from 0-100 indicating MaxMind's
      confidence that the country is correct. This attribute is only available
      from the Omni end point.
    :ivar geoname_id: This returns a GeoName ID for the country. This attribute
      is returned by all end points.
    :ivar iso_3166_1_alpha_2: This returns the two-character ISO 3166-1
      (http://en.wikipedia.org/wiki/ISO_3166-1) alpha code for the country.
      This attribute is returned by all end points.
    :ivar iso_3166_1_alpha_3: This returns the three-character ISO 3166-1
      (http://en.wikipedia.org/wiki/ISO_3166-1) alpha code for the country.
      This attribute is returned by all end points.
    :ivar name: Returns the name of the country based on the languages list
      passed to the constructor. This attribute is returned by all end points.
    :ivar names: This returns a dictionary where the keys are language codes
      and the values are names. This attribute is returned by all end points.

    """
    _valid_attributes = set(['confidence', 'geoname_id', 'iso_3166_1_alpha_2',
                             'iso_3166_1_alpha_3', 'names'])


class Location(Record):
    """Contains data for the location record associated with an IP address

    This class contains the location data associated with an IP address.

    This record is returned by all the end points except the Country end point.

    Attributes:

    :ivar accuracy_radius: This returns the radius in kilometers around the
      specified location where the IP address is likely to be. This attribute
      is only available from the Omni end point.
    :ivar latitude: This returns the latitude of the location as a floating
      point number. This attribute is returned by all end points except the
      Country end point.
    :ivar longitude: This returns the longitude of the location as a
      floating point number. This attribute is returned by all end points
      except the Country end point.
    :ivar metro_code: This returns the metro code of the location if the
      location is in the US. MaxMind returns the same metro codes as the
      Google AdWords API
      (https://developers.google.com/adwords/api/docs/appendix/cities-DMAregions).
      This attribute is returned by all end points except the Country end
      point.
    :ivar postal_code: This returns the postal code of the location. Postal
      codes are not available for all countries. In some countries, this will
      only contain part of the postal code. This attribute is returned by all
      end points except the Country end point.
    :ivar postal_confidence: This returns a value from 0-100 indicating
      MaxMind's confidence that the postal code is correct. This attribute is
      only available from the Omni end point.
    :ivar time_zone: This returns the time zone associated with location, as
      specified by the IANA Time Zone Database
      (http://www.iana.org/time-zones), e.g., "America/New_York". This
      attribute is returned by all end points except the Country end point.

    """
    _valid_attributes = set(['accuracy_radius', 'latitude', 'longitude'
                             'metro_code', 'postal_code', 'postal_confidence',
                             'time_zone'])


class Region(PlaceRecord):
    """Contains data for the region record associated with an IP address

    This class contains the region-level data associated with an IP address.

    This record is returned by all the end points except the Country end point.

    Attributes:

    :ivar confidence: This is a value from 0-100 indicating MaxMind's
      confidence that the region is correct. This attribute is only available
      from the Omni end point.
    :ivar geoname_id: This is a GeoName ID for the region. This attribute
      is returned by all end points.
    :ivar iso_3166_2: This is a string up to three characters long
      contain the region portion of the ISO 3166-2 code
      (http://en.wikipedia.org/wiki/ISO_3166-2). This attribute is returned
      by all end points.
    :ivar name: The name of the region based on the languages list
      passed to the constructor. This attribute is returned by all end points.
    :ivar names: A dictionary where the keys are language codes and the
      values are names. This attribute is returned by all end points.

    """
    _valid_attributes = set(['confidence', 'geoname_id', 'iso_3166_2',
                             'names'])


class Traits(Record):
    """ Contains data for the traits record associated with an IP address

    This class contains the traits data associated with an IP address.

    This record is returned by all the end points.

    This class has the following attributes:

    :ivar autonomous_system_number: This returns the autonomous system 
      number (http://en.wikipedia.org/wiki/Autonomous_system_(Internet))
      associated with the IP address. This attribute is only available from
      the City/ISP/Org and Omni end points.
    :ivar autonomous_system_organization: This returns the organization
      associated with the registered autonomous system number
      (http://en.wikipedia.org/wiki/Autonomous_system_(Internet)) for the IP
      address. This attribute is only available from the City/ISP/Org and
      Omni end points.
    :ivar domain: This returns the second level domain associated with the
      IP address. This will be something like "example.com" or
      "example.co.uk", not "foo.example.com". This attribute is only available
      from the City/ISP/Org and Omni end points.
    :ivar ip_address: This returns the IP address that the data in the model
      is for. If you performed a "me" lookup against the web service, this
      will be the externally routable IP address for the system the code is
      running on. If the system is behind a NAT, this may differ from the IP
      address locally assigned to it. This attribute is returned by all end
      points.
    :ivar is_anonymous_proxy: This returns true if the IP is an anonymous
      proxy. See http://dev.maxmind.com/faq/geoip#anonproxy for further
      details. This attribute is returned by all end points.
    :ivar is_transparent_proxy: This returns true if the IP is a transparent
      proxy. This attribute is returned by all end points.
    :ivar isp: This returns the name of the ISP associated the IP address.
      This attribute is only available from the City/ISP/Org and Omni end
      points.
    :ivar organization: This returns the name of the organization associated
      the IP address. This attribute is only available from the City/ISP/Org
      and Omni end points.
    :ivar user_type: This returns the user type associated with the IP
      address. This can be one of the following values:

      * business
      * cafe
      * cellular
      * college
      * content_delivery_network
      * dialup
      * government
      * hosting
      * library
      * military
      * residential
      * router
      * school
      * search_engine_spider
      * traveler

      This attribute is only available from the Omni end point.

"""
    _valid_attributes = set(['autonomous_system_number',
                             'autonomous_system_organization',
                             'domain',
                             'is_anonymous_proxy',
                             'is_satellite_provider',
                             'is_transparent_proxy',
                             'isp',
                             'ip_address',
                             'organization',
                             'user_type'])

    def __init__(self, languages=None, **kwargs):
        for k in ['is_anonymous_proxy', 'is_satellite_provider',
                  'is_transparent_proxy']:
            kwargs[k] = bool(kwargs.get(k, False))
        super(Traits, self).__init__(**kwargs)
