import geoip2.records


class Country(object):
    # Added **kwargs to ensure it doesn't break if we add a new top-level hash.
    # Empty dictionary as default argument is safe as we don't modify it.
    def __init__(self, languages=None, continent={}, country={},
                 registered_country={}, traits={}, **kwargs):
        self.continent = geoip2.records.Continent(languages, **continent)
        self.country = geoip2.records.Country(languages, **country)
        self.registered_country = geoip2.records.Country(languages,
                                                         **registered_country)
        self.traits = geoip2.records.Traits(languages, **traits)


class City(Country):
    def __init__(self, languages=None, city={}, continent={}, country={},
                 location={}, region={}, registered_country={}, traits={},
                 **kwargs):
        super().__init__(languages, continent, country, registered_country,
                         traits)
        self.city = geoip2.records.City(languages, **city)
        self.location = geoip2.records.Location(languages, **location)
        self.region = geoip2.records.Region(languages, **region)


class CityISPOrg(City):
    pass


class Omni(CityISPOrg):
    pass
