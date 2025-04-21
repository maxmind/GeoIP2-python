=========================
MaxMind GeoIP2 Python API
=========================

Description
-----------

This package provides an API for the GeoIP2 and GeoLite2 `web services
<https://dev.maxmind.com/geoip/docs/web-services?lang=en>`_ and `databases
<https://dev.maxmind.com/geoip/docs/databases?lang=en>`_.

Installation
------------

To install the ``geoip2`` module, type:

.. code-block:: bash

    $ pip install geoip2

If you are not able to install from PyPI, you may also use ``pip`` from the
source directory:

.. code-block:: bash

    $ python -m pip install .

Database Reader Extension
^^^^^^^^^^^^^^^^^^^^^^^^^

If you wish to use the C extension for the database reader, you must first
install the `libmaxminddb C API <https://github.com/maxmind/libmaxminddb>`_.
Please `see the instructions distributed with it
<https://github.com/maxmind/libmaxminddb/blob/main/README.md>`_.

IP Geolocation Usage
--------------------

IP geolocation is inherently imprecise. Locations are often near the center of
the population. Any location provided by a GeoIP2 database or web service
should not be used to identify a particular address or household.

Web Service Usage
-----------------

To use this API, you first construct either a ``geoip2.webservice.Client`` or
``geoip2.webservice.AsyncClient``, passing your MaxMind ``account_id`` and
``license_key`` to the constructor. To use the GeoLite2 web service instead of
the GeoIP2 web service, set the optional ``host`` keyword argument to
``geolite.info``. To use the Sandbox GeoIP2 web service instead of the
production GeoIP2 web service, set the optional ``host`` keyword argument to
``sandbox.maxmind.com``.

After doing this, you may call the method corresponding to request type
(e.g., ``city`` or ``country``), passing it the IP address you want to look up.

If the request succeeds, the method call will return a model class for the
endpoint you called. This model in turn contains multiple record classes,
each of which represents part of the data returned by the web service.

If the request fails, the client class throws an exception.

Sync Web Service Example
------------------------

.. code-block:: pycon

    >>> import geoip2.webservice
    >>>
    >>> # This creates a Client object that can be reused across requests.
    >>> # Replace "42" with your account ID and "license_key" with your license
    >>> # key. Set the "host" keyword argument to "geolite.info" to use the
    >>> # GeoLite2 web service instead of the GeoIP2 web service. Set the
    >>> # "host" keyword argument to "sandbox.maxmind.com" to use the Sandbox
    >>> # GeoIP2 web service instead of the production GeoIP2 web service.
    >>> with geoip2.webservice.Client(42, 'license_key') as client:
    >>>
    >>>     # Replace "city" with the method corresponding to the web service
    >>>     # that you are using, i.e., "country", "city", or "insights". Please
    >>>     # note that Insights is not supported by the GeoLite2 web service.
    >>>     response = client.city('203.0.113.0')
    >>>
    >>>     response.country.iso_code
    'US'
    >>>     response.country.name
    'United States'
    >>>     response.country.names['zh-CN']
    u'美国'
    >>>
    >>>     response.subdivisions.most_specific.name
    'Minnesota'
    >>>     response.subdivisions.most_specific.iso_code
    'MN'
    >>>
    >>>     response.city.name
    'Minneapolis'
    >>>
    >>>     response.postal.code
    '55455'
    >>>
    >>>     response.location.latitude
    44.9733
    >>>     response.location.longitude
    -93.2323
    >>>
    >>>     response.traits.network
    IPv4Network('203.0.113.0/32')

Async Web Service Example
-------------------------

.. code-block:: pycon

    >>> import asyncio
    >>>
    >>> import geoip2.webservice
    >>>
    >>> async def main():
    >>>     # This creates an AsyncClient object that can be reused across
    >>>     # requests on the running event loop. If you are using multiple event
    >>>     # loops, you must ensure the object is not used on another loop.
    >>>     #
    >>>     # Replace "42" with your account ID and "license_key" with your license
    >>>     # key. Set the "host" keyword argument to "geolite.info" to use the
    >>>     # GeoLite2 web service instead of the GeoIP2 web service. Set the
    >>>     # "host" keyword argument to "sandbox.maxmind.com" to use the Sandbox
    >>>     # GeoIP2 web service instead of the production GeoIP2 web service.
    >>>     async with geoip2.webservice.AsyncClient(42, 'license_key') as client:
    >>>
    >>>         # Replace "city" with the method corresponding to the web service
    >>>         # that you are using, i.e., "country", "city", or "insights". Please
    >>>         # note that Insights is not supported by the GeoLite2 web service.
    >>>         response = await client.city('203.0.113.0')
    >>>
    >>>         response.country.iso_code
    'US'
    >>>         response.country.name
    'United States'
    >>>         response.country.names['zh-CN']
    u'美国'
    >>>
    >>>         response.subdivisions.most_specific.name
    'Minnesota'
    >>>         response.subdivisions.most_specific.iso_code
    'MN'
    >>>
    >>>         response.city.name
    'Minneapolis'
    >>>
    >>>         response.postal.code
    '55455'
    >>>
    >>>         response.location.latitude
    44.9733
    >>>         response.location.longitude
    -93.2323
    >>>
    >>>         response.traits.network
    IPv4Network('203.0.113.0/32')
    >>>
    >>> asyncio.run(main())

Web Service Client Exceptions
-----------------------------

For details on the possible errors returned by the web service itself, see
https://dev.maxmind.com/geoip/docs/web-services?lang=en for the GeoIP2 web
service docs.

If the web service returns an explicit error document, this is thrown as a
``AddressNotFoundError``, ``AuthenticationError``, ``InvalidRequestError``, or
``OutOfQueriesError`` as appropriate. These all subclass ``GeoIP2Error``.

If some other sort of error occurs, this is thrown as an ``HTTPError``. This
is thrown when some sort of unanticipated error occurs, such as the web
service returning a 500 or an invalid error document. If the web service
returns any status code besides 200, 4xx, or 5xx, this also becomes an
``HTTPError``.

Finally, if the web service returns a 200 but the body is invalid, the client
throws a ``GeoIP2Error``.

Database Usage
--------------

To use the database API, you first construct a ``geoip2.database.Reader`` using
the path to the file as the first argument. After doing this, you may call the
method corresponding to database type (e.g., ``city`` or ``country``), passing it
the IP address you want to look up.

If the lookup succeeds, the method call will return a model class for the
database method you called. This model in turn contains multiple record classes,
each of which represents part of the data for the record.

If the request fails, the reader class throws an exception.

Database Example
----------------

City Database
^^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoLite2-City.mmdb') as reader:
    >>>
    >>>     # Replace "city" with the method corresponding to the database
    >>>     # that you are using, e.g., "country".
    >>>     response = reader.city('203.0.113.0')
    >>>
    >>>     response.country.iso_code
    'US'
    >>>     response.country.name
    'United States'
    >>>     response.country.names['zh-CN']
    u'美国'
    >>>
    >>>     response.subdivisions.most_specific.name
    'Minnesota'
    >>>     response.subdivisions.most_specific.iso_code
    'MN'
    >>>
    >>>     response.city.name
    'Minneapolis'
    >>>
    >>>     response.postal.code
    '55455'
    >>>
    >>>     response.location.latitude
    44.9733
    >>>     response.location.longitude
    -93.2323
    >>>
    >>>     response.traits.network
    IPv4Network('203.0.113.0/24')

Anonymous IP Database
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoIP2-Anonymous-IP.mmdb') as reader:
    >>>
    >>>     response = reader.anonymous_ip('203.0.113.0')
    >>>
    >>>     response.is_anonymous
    True
    >>>     response.is_anonymous_vpn
    False
    >>>     response.is_hosting_provider
    False
    >>>     response.is_public_proxy
    False
    >>>     response.is_residential_proxy
    False
    >>>     response.is_tor_exit_node
    True
    >>>     response.ip_address
    '203.0.113.0'
    >>>     response.network
    IPv4Network('203.0.113.0/24')

Anonymous Plus Database
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoIP-Anonymous-Plus.mmdb') as reader:
    >>>
    >>>     response = reader.anonymous_plus('203.0.113.0')
    >>>
    >>>     response.anonymizer_confidence
    30
    >>>     response.is_anonymous
    True
    >>>     response.is_anonymous_vpn
    True
    >>>     response.is_hosting_provider
    False
    >>>     response.is_public_proxy
    False
    >>>     response.is_residential_proxy
    False
    >>>     response.is_tor_exit_node
    False
    >>>     response.ip_address
    '203.0.113.0'
    >>>     response.network
    IPv4Network('203.0.113.0/24')
    >>>     response.network_last_seen
    datetime.date(2025, 4, 18)
    >>>     response.provider_name
    FooBar VPNs

ASN Database
^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoLite2-ASN.mmdb') as reader:
    >>>     response = reader.asn('203.0.113.0')
    >>>     response.autonomous_system_number
    1221
    >>>     response.autonomous_system_organization
    'Telstra Pty Ltd'
    >>>     response.ip_address
    '203.0.113.0'
    >>>     response.network
    IPv4Network('203.0.113.0/24')

Connection-Type Database
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoIP2-Connection-Type.mmdb') as reader:
    >>>     response = reader.connection_type('203.0.113.0')
    >>>     response.connection_type
    'Corporate'
    >>>     response.ip_address
    '203.0.113.0'
    >>>     response.network
    IPv4Network('203.0.113.0/24')


Domain Database
^^^^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoIP2-Domain.mmdb') as reader:
    >>>     response = reader.domain('203.0.113.0')
    >>>     response.domain
    'umn.edu'
    >>>     response.ip_address
    '203.0.113.0'

Enterprise Database
^^^^^^^^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoIP2-Enterprise.mmdb') as reader:
    >>>
    >>>     # Use the .enterprise method to do a lookup in the Enterprise database
    >>>     response = reader.enterprise('203.0.113.0')
    >>>
    >>>     response.country.confidence
    99
    >>>     response.country.iso_code
    'US'
    >>>     response.country.name
    'United States'
    >>>     response.country.names['zh-CN']
    u'美国'
    >>>
    >>>     response.subdivisions.most_specific.name
    'Minnesota'
    >>>     response.subdivisions.most_specific.iso_code
    'MN'
    >>>     response.subdivisions.most_specific.confidence
    77
    >>>
    >>>     response.city.name
    'Minneapolis'
    >>>     response.country.confidence
    11
    >>>
    >>>     response.postal.code
    '55455'
    >>>
    >>>     response.location.accuracy_radius
    50
    >>>     response.location.latitude
    44.9733
    >>>     response.location.longitude
    -93.2323
    >>>
    >>>     response.traits.network
    IPv4Network('203.0.113.0/24')


ISP Database
^^^^^^^^^^^^

.. code-block:: pycon

    >>> import geoip2.database
    >>>
    >>> # This creates a Reader object. You should use the same object
    >>> # across multiple requests as creation of it is expensive.
    >>> with geoip2.database.Reader('/path/to/GeoIP2-ISP.mmdb') as reader:
    >>>     response = reader.isp('203.0.113.0')
    >>>     response.autonomous_system_number
    1221
    >>>     response.autonomous_system_organization
    'Telstra Pty Ltd'
    >>>     response.isp
    'Telstra Internet'
    >>>     response.organization
    'Telstra Internet'
    >>>     response.ip_address
    '203.0.113.0'
    >>>     response.network
    IPv4Network('203.0.113.0/24')

Database Reader Exceptions
--------------------------

If the database file does not exist or is not readable, the constructor will
raise a ``FileNotFoundError`` or a ``PermissionError``. If the IP address passed
to a method is invalid, a ``ValueError`` will be raised. If the file is invalid
or there is a bug in the reader, a ``maxminddb.InvalidDatabaseError`` will be
raised with a description of the problem. If an IP address is not in the
database, a ``AddressNotFoundError`` will be raised.

``AddressNotFoundError`` references the largest subnet where no address would be
found. This can be used to efficiently enumerate entire subnets:

.. code-block:: python

    import geoip2.database
    import geoip2.errors
    import ipaddress

    # This creates a Reader object. You should use the same object
    # across multiple requests as creation of it is expensive.
    with geoip2.database.Reader('/path/to/GeoLite2-ASN.mmdb') as reader:
        network = ipaddress.ip_network("192.128.0.0/15")

        ip_address = network[0]
        while ip_address in network:
            try:
                response = reader.asn(ip_address)
                response_network = response.network
            except geoip2.errors.AddressNotFoundError as e:
                response = None
                response_network = e.network
            print(f"{response_network}: {response!r}")
            ip_address = response_network[-1] + 1  # move to next subnet

Values to use for Database or Dictionary Keys
---------------------------------------------

**We strongly discourage you from using a value from any ``names`` property as
a key in a database or dictionaries.**

These names may change between releases. Instead we recommend using one of the
following:

* ``geoip2.records.City`` - ``city.geoname_id``
* ``geoip2.records.Continent`` - ``continent.code`` or ``continent.geoname_id``
* ``geoip2.records.Country`` and ``geoip2.records.RepresentedCountry`` - ``country.iso_code`` or ``country.geoname_id``
* ``geoip2.records.subdivision`` - ``subdivision.iso_code`` or ``subdivision.geoname_id``

What data is returned?
----------------------

While many of the models contain the same basic records, the attributes which
can be populated vary between web service endpoints or databases. In
addition, while a model may offer a particular piece of data, MaxMind does not
always have every piece of data for any given IP address.

Because of these factors, it is possible for any request to return a record
where some or all of the attributes are unpopulated.

The only piece of data which is always returned is the ``ip_address``
attribute in the ``geoip2.records.Traits`` record.

Integration with GeoNames
-------------------------

`GeoNames <https://www.geonames.org/>`_ offers web services and downloadable
databases with data on geographical features around the world, including
populated places. They offer both free and paid premium data. Each feature is
uniquely identified by a ``geoname_id``, which is an integer.

Many of the records returned by the GeoIP web services and databases include a
``geoname_id`` field. This is the ID of a geographical feature (city, region,
country, etc.) in the GeoNames database.

Some of the data that MaxMind provides is also sourced from GeoNames. We
source things like place names, ISO codes, and other similar data from the
GeoNames premium data set.

Reporting Data Problems
-----------------------

If the problem you find is that an IP address is incorrectly mapped, please
`submit your correction to MaxMind <https://www.maxmind.com/en/correction>`_.

If you find some other sort of mistake, like an incorrect spelling, please
check the `GeoNames site <https://www.geonames.org/>`_ first. Once you've
searched for a place and found it on the GeoNames map view, there are a
number of links you can use to correct data ("move", "edit", "alternate
names", etc.). Once the correction is part of the GeoNames data set, it
will be automatically incorporated into future MaxMind releases.

If you are a paying MaxMind customer and you're not sure where to submit a
correction, please `contact MaxMind support
<https://www.maxmind.com/en/support>`_ for help.

Requirements
------------

Python 3.9 or greater is required. Older versions are not supported.

The Requests HTTP library is also required. See
<https://pypi.org/project/requests/> for details.

Versioning
----------

The GeoIP2 Python API uses `Semantic Versioning <https://semver.org/>`_.

Support
-------

Please report all issues with this code using the `GitHub issue tracker
<https://github.com/maxmind/GeoIP2-python/issues>`_

If you are having an issue with a MaxMind service that is not specific to the
client API, please contact `MaxMind support
<https://www.maxmind.com/en/support>`_ for assistance.
