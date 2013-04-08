class GeoIP2Error(RuntimeError):
    """There was a generic error in GeoIP2."""


class GeoIP2HTTPError(GeoIP2Error):
    """There was an error when making your HTTP request."""
    def __init__(self, message, http_status=None, uri=None):
        super().__init__(message)
        self.http_status = http_status
        self.uri = uri


class GeoIP2WebServiceError(GeoIP2HTTPError):
    """The GeoIP2 web service returned an error."""
    def __init__(self, message, code=None, http_status=None, uri=None):
        super().__init__(message, http_status, uri)
        self.code = code
