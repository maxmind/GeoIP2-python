"""Typed errors thrown by this library."""

import ipaddress
from typing import Optional, Union


class GeoIP2Error(RuntimeError):
    """There was a generic error in GeoIP2.

    This class represents a generic error. It extends :py:exc:`RuntimeError`
    and does not add any additional attributes.

    """


class AddressNotFoundError(GeoIP2Error):
    """The address you were looking up was not found."""

    ip_address: Optional[str]
    """The IP address used in the lookup. This is only available for database
    lookups.
    """
    _prefix_len: Optional[int]

    def __init__(
        self,
        message: str,
        ip_address: Optional[str] = None,
        prefix_len: Optional[int] = None,
    ) -> None:
        super().__init__(message)
        self.ip_address = ip_address
        self._prefix_len = prefix_len

    @property
    def network(self) -> Optional[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]:
        """The network associated with the error.

        In particular, this is the largest network where no address would be
        found. This is only available for database lookups.
        """
        if self.ip_address is None or self._prefix_len is None:
            return None
        return ipaddress.ip_network(
            f"{self.ip_address}/{self._prefix_len}", strict=False
        )


class AuthenticationError(GeoIP2Error):
    """There was a problem authenticating the request."""


class HTTPError(GeoIP2Error):
    """There was an error when making your HTTP request.

    This class represents an HTTP transport error. It extends
    :py:exc:`GeoIP2Error` and adds attributes of its own.

    """

    http_status: Optional[int]
    """The HTTP status code returned"""
    uri: Optional[str]
    """The URI queried"""
    decoded_content: Optional[str]
    """The decoded response content"""

    def __init__(
        self,
        message: str,
        http_status: Optional[int] = None,
        uri: Optional[str] = None,
        decoded_content: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.uri = uri
        self.decoded_content = decoded_content


class InvalidRequestError(GeoIP2Error):
    """The request was invalid."""


class OutOfQueriesError(GeoIP2Error):
    """Your account is out of funds for the service queried."""


class PermissionRequiredError(GeoIP2Error):
    """Your account does not have permission to access this service."""
