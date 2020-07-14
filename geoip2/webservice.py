"""
============================
WebServices Client API
============================

This class provides a client API for all the GeoIP2 Precision web service end
points. The end points are Country, City, and Insights. Each end point returns
a different set of data about an IP address, with Country returning the least
data and Insights the most.

Each web service end point is represented by a different model class, and
these model classes in turn contain multiple record classes. The record
classes have attributes which contain data about the IP address.

If the web service does not return a particular piece of data for an IP
address, the associated attribute is not populated.

The web service may not return any information for an entire record, in which
case all of the attributes for that record class will be empty.

SSL
---

Requests to the GeoIP2 Precision web service are always made with SSL.

"""

import ipaddress
from typing import Any, cast, List, Optional, Type, Union

import requests
from requests.models import Response
from requests.utils import default_user_agent

import geoip2
import geoip2.models
from geoip2.errors import (
    AddressNotFoundError,
    AuthenticationError,
    GeoIP2Error,
    HTTPError,
    InvalidRequestError,
    OutOfQueriesError,
    PermissionRequiredError,
)
from geoip2.models import City, Country, Insights
from geoip2.types import IPAddress


class BaseClient:  # pylint: disable=missing-class-docstring
    _account_id: str
    _host: str
    _license_key: str
    _locales: List[str]
    _timeout: Optional[float]
    _user_agent: str

    def __init__(
        self,
        account_id: int,
        license_key: str,
        host: str,
        locales: Optional[List[str]],
        timeout: Optional[float],
        http_user_agent: str,
    ) -> None:
        """Construct a Client."""
        # pylint: disable=too-many-arguments
        if locales is None:
            locales = ["en"]

        self._locales = locales
        # requests 2.12.2 requires that the username passed to auth be bytes
        # or a string, with the former being preferred.
        self._account_id = (
            account_id if isinstance(account_id, bytes) else str(account_id)
        )
        self._license_key = license_key
        self._base_uri = "https://%s/geoip/v2.1" % host
        self._timeout = timeout
        self._user_agent = "GeoIP2-Python-Client/%s %s" % (
            geoip2.__version__,
            http_user_agent,
        )

    def city(self, ip_address: IPAddress = "me") -> City:
        """Call GeoIP2 Precision City endpoint with the specified IP.

        :param ip_address: IPv4 or IPv6 address as a string. If no
           address is provided, the address that the web service is
           called from will be used.

        :returns: :py:class:`geoip2.models.City` object

        """
        return cast(City, self._response_for("city", geoip2.models.City, ip_address))

    def country(self, ip_address: IPAddress = "me") -> Country:
        """Call the GeoIP2 Country endpoint with the specified IP.

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Country` object

        """
        return cast(
            Country, self._response_for("country", geoip2.models.Country, ip_address)
        )

    def insights(self, ip_address: IPAddress = "me") -> Insights:
        """Call the GeoIP2 Precision: Insights endpoint with the specified IP.

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Insights` object

        """
        return cast(
            Insights, self._response_for("insights", geoip2.models.Insights, ip_address)
        )

    def _response_for(
        self,
        path: str,
        model_class: Union[Type[Insights], Type[City], Type[Country]],
        ip_address: IPAddress,
    ) -> Union[Country, City, Insights]:
        if ip_address != "me":
            ip_address = ipaddress.ip_address(ip_address)
        uri = "/".join([self._base_uri, path, str(ip_address)])
        response = requests.get(
            uri,
            auth=(self._account_id, self._license_key),
            headers={"Accept": "application/json", "User-Agent": self._user_agent},
            timeout=self._timeout,
        )
        if response.status_code != 200:
            raise self._exception_for_error(response, uri)
        body = self._handle_success(response, uri)
        return model_class(body, locales=self._locales)

    @staticmethod
    def _handle_success(response: Response, uri: str) -> Any:
        try:
            return response.json()
        except ValueError as ex:
            raise GeoIP2Error(
                "Received a 200 response for %(uri)s"
                " but could not decode the response as "
                "JSON: " % locals() + ", ".join(ex.args),
                200,
                uri,
            )

    def _exception_for_error(self, response: Response, uri: str) -> GeoIP2Error:
        status = response.status_code

        if 400 <= status < 500:
            return self._exception_for_4xx_status(response, status, uri)
        if 500 <= status < 600:
            return self._exception_for_5xx_status(status, uri)
        return self._exception_for_non_200_status(status, uri)

    def _exception_for_4xx_status(
        self, response: Response, status: int, uri: str
    ) -> GeoIP2Error:
        if not response.content:
            return HTTPError(
                "Received a %(status)i error for %(uri)s " "with no body." % locals(),
                status,
                uri,
            )
        if response.headers["Content-Type"].find("json") == -1:
            return HTTPError(
                "Received a %i for %s with the following "
                "body: %s" % (status, uri, str(response.content)),
                status,
                uri,
            )
        try:
            body = response.json()
        except ValueError as ex:
            return HTTPError(
                "Received a %(status)i error for %(uri)s but it did"
                " not include the expected JSON body: " % locals() + ", ".join(ex.args),
                status,
                uri,
            )
        else:
            if "code" in body and "error" in body:
                return self._exception_for_web_service_error(
                    body.get("error"), body.get("code"), status, uri
                )
            return HTTPError(
                "Response contains JSON but it does not specify " "code or error keys",
                status,
                uri,
            )

    @staticmethod
    def _exception_for_web_service_error(
        message: str, code: str, status: int, uri: str
    ) -> Union[
        AuthenticationError,
        AddressNotFoundError,
        PermissionRequiredError,
        OutOfQueriesError,
        InvalidRequestError,
    ]:
        if code in ("IP_ADDRESS_NOT_FOUND", "IP_ADDRESS_RESERVED"):
            return AddressNotFoundError(message)
        if code in (
            "ACCOUNT_ID_REQUIRED",
            "ACCOUNT_ID_UNKNOWN",
            "AUTHORIZATION_INVALID",
            "LICENSE_KEY_REQUIRED",
            "USER_ID_REQUIRED",
            "USER_ID_UNKNOWN",
        ):
            return AuthenticationError(message)
        if code in ("INSUFFICIENT_FUNDS", "OUT_OF_QUERIES"):
            return OutOfQueriesError(message)
        if code == "PERMISSION_REQUIRED":
            return PermissionRequiredError(message)

        return InvalidRequestError(message, code, status, uri)

    @staticmethod
    def _exception_for_5xx_status(status: int, uri: str) -> HTTPError:
        return HTTPError(
            "Received a server error (%(status)i) for " "%(uri)s" % locals(),
            status,
            uri,
        )

    @staticmethod
    def _exception_for_non_200_status(status: int, uri: str) -> HTTPError:
        return HTTPError(
            "Received a very surprising HTTP status "
            "(%(status)i) for %(uri)s" % locals(),
            status,
            uri,
        )


class Client(BaseClient):
    """A synchronous GeoIP2 client.

    It accepts the following required arguments:

    :param account_id: Your MaxMind account ID.
    :param license_key: Your MaxMind license key.

    Go to https://www.maxmind.com/en/my_license_key to see your MaxMind
    account ID and license key.

    The following keyword arguments are also accepted:

    :param host: The hostname to make a request against. This defaults to
      "geoip.maxmind.com". In most cases, you should not need to set this
      explicitly.
    :param locales: This is list of locale codes. This argument will be
      passed on to record classes to use when their name properties are
      called. The default value is ['en'].

      The order of the locales is significant. When a record class has
      multiple names (country, city, etc.), its name property will return
      the name in the first locale that has one.

      Note that the only locale which is always present in the GeoIP2
      data is "en". If you do not include this locale, the name property
      may end up returning None even when the record has an English name.

      Currently, the valid locale codes are:

      * de -- German
      * en -- English names may still include accented characters if that is
        the accepted spelling in English. In other words, English does not
        mean ASCII.
      * es -- Spanish
      * fr -- French
      * ja -- Japanese
      * pt-BR -- Brazilian Portuguese
      * ru -- Russian
      * zh-CN -- Simplified Chinese.
    :param timeout: The timeout to use when waiting on the request. This sets
      both the connect timeout and the read timeout.

    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        account_id: int,
        license_key: str,
        host: str = "geoip.maxmind.com",
        locales: Optional[List[str]] = None,
        timeout: Optional[float] = None,
    ) -> None:
        super().__init__(
            account_id, license_key, host, locales, timeout, default_user_agent()
        )

    def _response_for(
        self,
        path: str,
        model_class: Union[Type[Insights], Type[City], Type[Country]],
        ip_address: IPAddress,
    ) -> Union[Country, City, Insights]:
        if ip_address != "me":
            ip_address = ipaddress.ip_address(ip_address)
        uri = "/".join([self._base_uri, path, str(ip_address)])
        response = requests.get(
            uri,
            auth=(self._account_id, self._license_key),
            headers={"Accept": "application/json", "User-Agent": self._user_agent},
            timeout=self._timeout,
        )
        if response.status_code != 200:
            raise self._exception_for_error(response, uri)
        body = self._handle_success(response, uri)
        return model_class(body, locales=self._locales)
