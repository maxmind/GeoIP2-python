from abc import ABCMeta


class Record(object):
    __metaclass__ = ABCMeta

    def __init__(self, **args):
        self.__dict__.update({k: args.get(k) for k in self._valid_attributes})

    def __setattr__(self, name, value):
        raise NotImplementedError(name + ' is read-only.')


class PlaceRecord(Record):
    __metaclass__ = ABCMeta

    # XXX - why did we name it 'name' instead of 'names'?
    def __init__(self, languages=None, **args):
        if languages is None:
            languages=[]
        object.__setattr__(self, 'languages', languages)
        args['names'] = args.pop('name', None)
        super().__init__(**args)

    @property
    def name(self):
        return next((self.names.get(x) for x in self.languages if x in
                     self.names), None)


class City(PlaceRecord):
    _valid_attributes = {'confidence', 'geoname_id', 'names'}


class Continent(PlaceRecord):
    _valid_attributes = {'continent_code', 'geoname_id', 'names'}


class Country(PlaceRecord):
    _valid_attributes = {'confidence', 'geoname_id', 'iso_3166_1_alpha_2',
                         'iso_3166_1_alpha_3', 'names'}


class Location(Record):
    _valid_attributes = {'accuracy_radius', 'latitude', 'longitude'
                         'metro_code', 'postal_code', 'postal_confidence',
                         'time_zone'}


class Region(PlaceRecord):
    _valid_attributes = {'confidence', 'geoname_id', 'iso_3166_2', 'names'}


class Traits(Record):
    _valid_attributes = {'autonomous_system_number',
                         'autonomous_system_organization',
                         'domain',
                         'is_anonymous_proxy',
                         'is_satellite_provider',
                         'is_transparent_proxy',
                         'isp',
                         'ip_address',
                         'organization',
                         'user_type'}
