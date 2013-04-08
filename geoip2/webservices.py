import geoip2.models
import requests
from .errors import GeoIP2Error, GeoIP2HTTPError, GeoIP2WebServiceError


class Client(object):
    def __init__(self, user_id, license_key, host='geoip.maxmind.com'):
        self.user_id = user_id
        self.license_key = license_key
        self._base_uri = 'https://%s/geoip' % (host)

    def city(self, ip='me'):
        return self._response_for('city', geoip2.models.City, ip)

    def city_isp_org(self, ip='me'):
        return self._response_for('city_isp_org', geoip2.models.CityISPOrg, ip)

    def country(self, ip='me'):
        return self._response_for('country', geoip2.models.Country, ip)

    def omni(self, ip='me'):
        return self._response_for('omni', geoip2.models.Omni, ip)

    def _response_for(self, path, model_class, ip):
        uri = '/'.join([self._base_uri, path, ip])
        response = requests.get(uri, auth=(self.user_id, self.license_key),
                                headers={'Accept': 'application/json'})
        if (response.status_code == 200):
            body = self._handle_success(response, uri)
            return model_class(**body)
        else:
            self._handle_error(response, uri)

    def _handle_success(self, response, uri):
        try:
            return response.json()
        except ValueError as e:
            raise GeoIP2HTTPError('Received a 200 response for %(uri)s'
                                  ' but could not decode the response as '
                                  'JSON: ' % locals() +
                                  ', '.join(e.args), 200, uri)

    def _handle_error(self, response, uri):
        status = response.status_code

        if status >= 400 and status < 499:
            self._handle_4xx_status(response, status, uri)
        elif status >= 500 and status < 599:
            self._handle_5xx_status(response, status, uri)
        else:
            self._handle_non_200_status(response, status, uri)

    def _handle_4xx_status(self, response, status, uri):
        if response.content:
            try:
                body = response.json()
            except ValueError as e:
                raise GeoIP2HTTPError(
                    'Received a %(status)i error for %(uri)s but it did'
                    ' not include the expected JSON body: ' % locals() +
                    ', '.join(e.args), status, uri)
            else:
                if 'code' in body and 'error' in body:
                    raise GeoIP2WebServiceError(body.get('error'),
                                                body.get('code'),
                                                status, uri)
                else:
                    raise GeoIP2HTTPError(
                        'Response contains JSON but it does not specify '
                        'code or error keys', status, uri)
        else:
            raise GeoIP2HTTPError('Received a %(status)i error for %(uri)s '
                                  'with no body.' % locals(), status, uri)

    def _handle_5xx_status(self, response, status, uri):
        raise GeoIP2HTTPError('Received a server error (%(status)i) for '
                              '%(uri)s' % locals(), status, uri)

    def _handle_non_200_status(self, response, status, uri):
        raise GeoIP2HTTPError('Received a very surprising HTTP status '
                              '(%(status)i) for %(uri)s' % locals(), status,
                              uri)
