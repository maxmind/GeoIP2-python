import geoip2.records


class Country(object):
    def __init__(self, raw_response, languages=None):
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
        self.traits = geoip2.records.Traits(languages,
                                            **raw_response.get('traits', {}))
        self.raw = raw_response


class City(Country):
    def __init__(self, raw_response, languages=None):
        super().__init__(raw_response, languages)
        self.city = \
            geoip2.records.City(languages, **raw_response.get('city', {}))
        self.location = \
            geoip2.records.Location(languages,
                                    **raw_response.get('location', {}))
        self.region = \
            geoip2.records.Region(languages,
                                  **raw_response.get('region', {}))


class CityISPOrg(City):
    pass


class Omni(CityISPOrg):
    pass
