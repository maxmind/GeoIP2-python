"""
Models
======

These classes provide models for the data returned by the GeoIP2
end points.

The only difference between the City, City/ISP/Org, and Omni model classes is
which fields in each record may be populated. See
http://dev.maxmind.com/geoip/geoip2/web-services for more details.

"""
#pylint:disable=R0903
import geoip2.records


class Country(object):
    """Model class for the GeoIP2 Country end point

    This class provides the following methods, each of which returns a record
    object.

    :ivar continent: :py:class:`geoip2.records.Continent` object
      representing continent data for the requested IP address.
    :ivar country: :py:class:`geoip2.records.Country` object representing
      country data for the requested IP address. This record represents the
      country where MaxMind believes the IP is located in.
    :ivar registered_country: :py:class:`geoip2.records.Country` object
      representing the registered country data for the requested IP address.
      This record represents the country where the ISP has registered a given
      IP block in and may differ from the user's country.
    :ivar represented_country: :py:class:`geoip2.records.RepresentedCountry`
      object containing details about the country represented by the users
      of the IP address when that country is different than the country in
      ``country``. For instance, the country represented by an
      overseas military base or embassy.
    :ivar traits: :py:class:`geoip2.records.Traits` object representing
      the traits for the request IP address.

    """
    def __init__(self, raw_response, languages=None):
        if languages is None:
            languages = ['en']
        self.continent = \
            geoip2.records.Continent(languages,
                                     **raw_response.get('continent', {}))
        self.country = \
            geoip2.records.Country(languages,
                                   **raw_response.get('country', {}))
        self.registered_country = \
            geoip2.records.Country(languages,
                                   **raw_response.get('registered_country',
                                                      {}))
        self.represented_country \
            = geoip2.records.RepresentedCountry(languages,
                                                **raw_response.get(
                                                'represented_country', {}))

        self.traits = geoip2.records.Traits(**raw_response.get('traits', {}))
        self.raw = raw_response


class City(Country):
    """Model class for the GeoIP2 Precision City end point

    :ivar city: :py:class:`geoip2.records.City` object representing
      country data for the requested IP address.
    :ivar continent: :py:class:`geoip2.records.Continent` object
      representing continent data for the requested IP address.
    :ivar country: :py:class:`geoip2.records.Country` object representing
      country data for the requested IP address. This record represents the
      country where MaxMind believes the IP is located in.
    :ivar location: :py:class:`geoip2.records.Location` object
      representing country data for the requested IP address.
    :ivar region: :py:class:`geoip2.records.Region` object representing
      country data for the requested IP address.
    :ivar registered_country: :py:class:`geoip2.records.Country` object
      representing the registered country data for the requested IP address.
      This record represents the country where the ISP has registered a given
      IP block in and may differ from the user's country.
    :ivar represented_country: :py:class:`geoip2.records.RepresentedCountry`
      object containing details about the country represented by the users
      of the IP address when that country is different than the country in
      ``country``. For instance, the country represented by an
      overseas military base or embassy.
    :ivar traits: :py:class:`geoip2.records.Traits` object representing
      the traits for the request IP address.

"""
    def __init__(self, raw_response, languages=None):
        super(City, self).__init__(raw_response, languages)
        self.city = \
            geoip2.records.City(languages, **raw_response.get('city', {}))
        self.location = \
            geoip2.records.Location(**raw_response.get('location', {}))
        self.postal = \
            geoip2.records.Postal(**raw_response.get('postal', {}))
        self.subdivisions = \
            geoip2.records.Subdivisions(languages,
                                        *raw_response.get('subdivisions', []))


class CityISPOrg(City):
    """Model class for the GeoIP2 Precision City/ISP/Org end point

    :ivar city: :py:class:`geoip2.records.City` object representing
      country data for the requested IP address.
    :ivar continent: :py:class:`geoip2.records.Continent` object
      representing continent data for the requested IP address.
    :ivar country: :py:class:`geoip2.records.Country` object representing
      country data for the requested IP address. This record represents the
      country where MaxMind believes the IP is located in.
    :ivar location: :py:class:`geoip2.records.Location` object
      representing country data for the requested IP address.
    :ivar region: :py:class:`geoip2.records.Region` object representing
      country data for the requested IP address.
    :ivar registered_country: :py:class`geoip2.records.Country` object
      representing the registered country data for the requested IP address.
      This record represents the country where the ISP has registered a given
      IP block in and may differ from the user's country.
    :ivar represented_country: :py:class:`geoip2.records.RepresentedCountry`
      object containing details about the country represented by the users
      of the IP address when that country is different than the country in
      ``country``. For instance, the country represented by an
      overseas military base or embassy.
    :ivar traits: :py:class:`geoip2.records.Traits` object representing
      the traits for the request IP address.

    """


class Omni(CityISPOrg):
    """Model class for the GeoIP2 Precision Omni end point

    :ivar city: :py:class:`geoip2.records.City` object representing
      country data for the requested IP address.
    :ivar continent: :py:class:`geoip2.records.Continent` object
      representing continent data for the requested IP address.
    :ivar country: :py:class:`geoip2.records.Country` object representing
      country data for the requested IP address. This record represents the
      country where MaxMind believes the IP is located in.
    :ivar location: :py:class:`geoip2.records.Location` object
      representing country data for the requested IP address.
    :ivar region: :py:class:`geoip2.records.Region` object representing
      country data for the requested IP address.
    :ivar registered_country: :py:class:`geoip2.records.Country` object
      representing the registered country data for the requested IP address.
      This record represents the country where the ISP has registered a given
      IP block in and may differ from the user's country.
    :ivar represented_country: :py:class:`geoip2.records.RepresentedCountry`
      object containing details about the country represented by the users
      of the IP address when that country is different than the country in
      ``country``. For instance, the country represented by an
      overseas military base or embassy.
    :ivar traits: :py:class:`geoip2.records.Traits` object representing
      the traits for the request IP address.

    """
