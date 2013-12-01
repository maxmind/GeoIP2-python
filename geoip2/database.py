"""
======================
GeoIP2 Database Reader
======================

"""
import geoip2
import geoip2.models
import maxminddb


class Reader(object):

    """Creates a new GeoIP2 database Reader object.

    Instances of this class provide a reader for the GeoIP2 database format.
    IP addresses can be looked up using the ``country`` and ``city`` methods.
    We also provide ``city_isp_org`` and ``omni`` methods to ease
    compatibility with the web service client, although we may offer the
    ability to specify additional databases to replicate these web services in
    the future (e.g., the ISP/Org database).

     Usage
     -----

    The basic API for this class is the same for every database. First, you
    create a reader object, specifying a file name. You then call the method
    corresponding to the specific database, passing it the IP address you want
    to look up.

    If the request succeeds, the method call will return a model class for the
    method you called. This model in turn contains multiple record classes,
    each of which represents part of the data returned by the database. If the
    database does not contain the requested information, the attributes on the
    record class will have a ``None`` value.

    If the address is not in the database, an
    ``geoip2.errors.AddressNotFoundError`` exception will be thrown. If the
    database is corrupt or invalid, a ``maxminddb.InvalidDatabaseError`` will
    be thrown.

"""

    def __init__(self, filename, locales=None):
        if locales is None:
            locales = ['en']
        self.db_reader = maxminddb.Reader(filename)
        self.locales = locales

    def country(self, ip_address):
        """Get the Country record object for the IP address

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Country` object

        """

        return self._model_for(geoip2.models.Country, ip_address)

    def city(self, ip_address):
        """Get the City record object for the IP address

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.City` object

        """
        return self._model_for(geoip2.models.City, ip_address)

    def city_isp_org(self, ip_address):
        """Get the CityISPOrg record object for the IP address

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.CityISPOrg` object

        """

        return self._model_for(geoip2.models.CityISPOrg, ip_address)

    def omni(self, ip_address):
        """Get the Omni record object for the IP address

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Omni` object

        """
        return self._model_for(geoip2.models.Omni, ip_address)

    def _model_for(self, model_class, ip_address):
        record = self.db_reader.get(ip_address)
        if record is None:
            raise geoip2.errors.AddressNotFoundError(
                "The address %s is not in the database." % ip_address)
        record.setdefault('traits', {})['ip_address'] = ip_address
        return model_class(record, locales=self.locales)

    def close(self):
        """Closes the GeoIP2 database"""

        self.db_reader.close()
