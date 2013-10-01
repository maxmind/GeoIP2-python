"""
======================
GeoIP2 Database Reader
======================

"""
import maxminddb
import geoip2.models


class Reader(object):

    """Creates a new GeoIP2 database Reader object."""

    def __init__(self, filename, languages=None):
        if languages is None:
            languages = ['en']
        self.db_reader = maxminddb.Reader(filename)
        self.languages = languages

    def country(self, ip_address):
        """Get the Country record object for the IP address"""

        return self._model_for(geoip2.models.Country, ip_address)

    def city(self, ip_address):
        """Get the City record object for the IP address"""
        return self._model_for(geoip2.models.City, ip_address)

    def city_isp_org(self, ip_address):
        """Get the CityISPOrg record object for the IP address"""

        return self._model_for(geoip2.models.CityISPOrg, ip_address)

    def omni(self, ip_address):
        """Get the Omni record object for the IP address"""
        return self._model_for(geoip2.models.Omni, ip_address)

    def _model_for(self, model_class, ip_address):
        record = self.db_reader.get(ip_address)
        if record is None:
            raise geoip2.errors.AddressNotFoundError(
                "The address %s is not in the database." % (ip_address))
        record.setdefault('traits', {})['ip_address'] = ip_address
        return model_class(record, languages=self.languages)

    def close(self):
        """Closes the Get the CityISPOrg record object for the IP address"""

        self.db_reader.close()
