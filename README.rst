=========================
MaxMind GeoIP2 Python API
=========================

Beta Note
---------
This is a beta release. The API may change before the first production
release, which will be numbered 2.0.0.

You may find information on the GeoIP2 beta release process on `our
website <http://www.maxmind.com/en/geoip2_beta>`_.

To provide feedback or get support during the beta, please see the
`MaxMind Customer Community <https://getsatisfaction.com/maxmind>`_.

Description
-----------

Currently, this distribution provides an API for the `GeoIP2 web services
<http://dev.maxmind.com/geoip/geoip2/web-services>`_.

In the future, this distribution will also provide the same API for the GeoIP2
downloadable databases. These databases have not yet been released as a
downloadable product.

See geoip2.webservices.Client for details on the web service client API.

Integration with GeoNames
-------------------------

`GeoNames <http://www.geonames.org/>`_ offers web services and downloadable
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
`submit your correction to MaxMind <http://www.maxmind.com/en/correction>`_.

If you find some other sort of mistake, like an incorrect spelling, please
check the `GeoNames site <http://www.geonames.org/>`_ first. Once you've
searched for a place and found it on the GeoNames map view, there are a
number of links you can use to correct data ("move", "edit", "alternate
names", etc.). Once the correction is part of the GeoNames data set, it
will be automatically incorporated into future MaxMind releases.

If you are a paying MaxMind customer and you're not sure where to submit a
correction, please `contact MaxMind support
<http://www.maxmind.com/en/support>`_ for help.

Python version support
----------------------

This code requires Python 2.6+ or 3.3+. Older versions are not supported.

Versioning
----------

The GeoIP2 Python API uses `Semantic Versioning <http://semver.org/>`_.

Support
-------

Please report all issues with this code using the `GitHub issue tracker
<https://github.com/maxmind/GeoIP2-python/issues>`_

If you are having an issue with a MaxMind service that is not specific to the
client API, please contact `MaxMind support
<http://www.maxmind.com/en/support>`_ for assistance.
