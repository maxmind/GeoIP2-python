.. :changelog:

History
-------

0.4.2 (2013-12-20)
++++++++++++++++++

* Added missing geoip2.models import to geoip.database.
* Documentation updates.

0.4.1 (2013-10-25)
++++++++++++++++++

* Read in `README.rst` as UTF-8 in `setup.py`.

0.4.0 (2013-10-21)
++++++++++++++++++

* API CHANGE: Changed the `languages` keyword argument to `locales` on the
  constructors for `geoip.webservice.Client` and `geoip.database.Reader`.

0.3.1 (2013-10-15)
++++++++++++++++++

* Fixed packaging issue with extras_require.

0.3.0 (2013-10-15)
++++++++++++++++++

* IMPORTANT: `geoip.webservices` was renamed `geoip.webservice` as it
  contains only one class.
* Added GeoIP2 database reader using maxminddb. This does not work with PyPy
  as it relies on a C extension.
* Added more specific exceptions for web service client.

0.2.2 (2013-06-20)
++++++++++++++++++

* Fixed a bug in the model objects that prevented `longitude` and `metro_code`
  from being used.

0.2.1 (2013-06-10)
++++++++++++++++++

* First official beta release.
* Documentation updates and corrections.

0.2.0 (2013-05-29)
++++++++++++++++++

* Support for Python 3.2 was dropped.
* The methods to call the web service on the `Client` object now validate
  the IP addresses before calling the web service. This requires the
  `ipaddr` module on Python 2.x.
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
