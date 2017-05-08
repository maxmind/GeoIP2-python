.. :changelog:

History
-------

2.5.0
++++++++++++++++++

* Added support for GeoLite2 ASN database.
* Correct documentation of errors raised when using the database reader.
  Reported by Radek Holý. GitHub #42.

2.4.2 (2016-12-08)
++++++++++++++++++

* Recent releases of ``requests`` (2.12.2 and 2.12.3) require that the
  username for basic authentication be a string or bytes. The documentation
  for this module uses an integer for the ``user_id``, which will break with
  these ``requests`` versions. The ``user_id`` is now converted to bytes
  before being passed to ``requests``.

2.4.1 (2016-11-21)
++++++++++++++++++

* Updated documentation to clarify what the accuracy radius refers to.
* Fixed classifiers in ``setup.py``.

2.4.0 (2016-06-10)
++++++++++++++++++

* This module now uses ``ipaddress`` on Python 2 rather than ``ipaddr`` to
  validate IP addresses before sending them to the web service.
* Added handling of additional error codes that the web service may return.
* PEP 257 documentation fixes.
* Updated documentation to reflect that the accuracy radius is now included
  in City.
* Previously, the source distribution was missing some tests and test
  databases. This has been corrected. Reported by Lumir Balhar.

2.3.0 (2016-04-15)
++++++++++++++++++

* Added support for the GeoIP2 Enterprise database.
* ``geoip2.database.Reader`` now supports being used in a ``with`` statement
  (PEP 343). (PR from Nguyễn Hồng Quân. GitHub #29)

2.2.0 (2015-06-29)
++++++++++++++++++

* The ``geoip2.records.Location` class has been updated to add attributes for
  the ``average_income`` and ``population_density`` fields provided by the
  Insights web service.
* The ``is_anonymous_proxy`` and ``is_satellite_provider`` properties on
  ``geoip2.records.Traits`` have been deprecated. Please use our `GeoIP2
  Anonymous IP database
  <https://www.maxmind.com/en/geoip2-anonymous-ip-database>`_
  to determine whether an IP address is used by an anonymizing service.

2.1.0 (2014-12-09)
++++++++++++++++++

* The reader now supports pure Python file and memory modes. If you are not
  using the C extension and your Python does not provide the ``mmap`` module,
  the file mode will be used by default. You can explicitly set the mode using
  the ``mode`` keyword argument with the ``MODE_AUTO``, ``MODE_MMAP``,
  ``MODE_MMAP_EXT``, ``MODE_FILE``, and ``MODE_MEMORY`` constants exported  by
  ``geoip2.database``.

2.0.2 (2014-10-28)
++++++++++++++++++

* Added support for the GeoIP2 Anonymous IP database. The
  ``geoip2.database.Reader`` class now has an ``anonymous_ip()`` method which
  returns a ``geoip2.models.AnonymousIP`` object.
* Added ``__repr__`` and ``__eq__`` methods to the model and record classes
  to aid in debugging and using the library from a REPL.

2.0.1 (2014-10-17)
++++++++++++++++++

* The constructor for ``geoip2.webservice.Client`` now takes an optional
  ``timeout`` parameter. (PR from arturro. GitHub #15)

2.0.0 (2014-09-22)
++++++++++++++++++

* First production release.

0.7.0 (2014-09-15)
++++++++++++++++++

* BREAKING CHANGES:
  - The deprecated ``city_isp_org()`` and ``omni()`` methods
    have been removed.
  - The ``geoip2.database.Reader`` lookup methods (e.g., ``city()``,
    ``isp()``) now raise a ``TypeError`` if they are used with a database that
    does not match the method. In particular, doing a ``city()`` lookup on a
    GeoIP2 Country database will result in an error and vice versa.
* A ``metadata()`` method has been added to the ``geoip2.database.Reader``
  class. This returns a ``maxminddb.reader.Metadata`` object with information
  about the database.

0.6.0 (2014-07-22)
++++++++++++++++++

* The web service client API has been updated for the v2.1 release of the web
  service. In particular, the ``city_isp_org`` and ``omni`` methods on
  ``geoip2.webservice.Client`` should be considered deprecated. The ``city``
  method now provides all of the data formerly provided by ``city_isp_org``,
  and the ``omni`` method has been replaced by the ``insights`` method.
  **Note:** In v2.1 of the web service, ``accuracy_radius``,
  ``autonomous_system_number``, and all of the ``confidence`` values were
  changed from unicode to integers. This may affect how you use these values
  from this API.
* Support was added for the GeoIP2 Connection Type, Domain, and ISP databases.

0.5.1 (2014-03-28)
++++++++++++++++++

* Switched to Apache 2.0 license.

0.5.0 (2014-02-11)
++++++++++++++++++

* Fixed missing import statements for geoip2.errors and geoip2.models.
  (Gustavo J. A. M. Carneiro)
* Minor documentation and code cleanup
* Added requirement for maxminddb v0.3.0, which includes a pure Python
  database reader. Removed the ``extras_require`` for maxminddb.

0.4.2 (2013-12-20)
++++++++++++++++++

* Added missing geoip2.models import to geoip.database.
* Documentation updates.

0.4.1 (2013-10-25)
++++++++++++++++++

* Read in ``README.rst`` as UTF-8 in ``setup.py``.

0.4.0 (2013-10-21)
++++++++++++++++++

* API CHANGE: Changed the ``languages`` keyword argument to ``locales`` on the
  constructors for ``geoip.webservice.Client`` and ``geoip.database.Reader``.

0.3.1 (2013-10-15)
++++++++++++++++++

* Fixed packaging issue with extras_require.

0.3.0 (2013-10-15)
++++++++++++++++++

* IMPORTANT: ``geoip.webservices`` was renamed ``geoip.webservice`` as it
  contains only one class.
* Added GeoIP2 database reader using ``maxminddb``. This does not work with
  PyPy as it relies on a C extension.
* Added more specific exceptions for web service client.

0.2.2 (2013-06-20)
++++++++++++++++++

* Fixed a bug in the model objects that prevented ``longitude`` and
  ``metro_code`` from being used.

0.2.1 (2013-06-10)
++++++++++++++++++

* First official beta release.
* Documentation updates and corrections.

0.2.0 (2013-05-29)
++++++++++++++++++

* Support for Python 3.2 was dropped.
* The methods to call the web service on the ``Client`` object now validate
  the IP addresses before calling the web service. This requires the
  ``ipaddr`` module on Python 2.x.
* We now support more languages. The new languages are de, es, fr, and pt-BR.
* The REST API now returns a record with data about your account. There is
  a new geoip.records.MaxMind class for this data.
* Rename model.continent.continent_code to model.continent.code.
* Documentation updates.

0.1.1 (2013-05-14)
++++++++++++++++++

* Documentation and packaging updates

0.1.0 (2013-05-13)
++++++++++++++++++

* Initial release
