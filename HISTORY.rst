.. :changelog:

History
-------

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
