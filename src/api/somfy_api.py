from requests_oauthlib import OAuth2Session

from src.api.model import Device
from src.api.model import Site

SOMFY_OAUTH = 'https://accounts.somfy.com/oauth/oauth/v2/auth'
SOMFY_TOKEN = 'https://accounts.somfy.com/oauth/oauth/v2/token'
SOMFY_REFRESH = 'https://accounts.somfy.com/oauth/oauth/v2/token'


class SomfyApi:
    __slots__ = '__oauth'

    def __init__(self, client_id, redirect_uri):
        self.__oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, auto_refresh_url=SOMFY_REFRESH)

    def get_authorization_url(self):
        return self.__oauth.authorization_url(SOMFY_OAUTH)

    def request_token(self, authorization_response, client_secret):
        return self.__oauth.fetch_token(
            SOMFY_TOKEN,
            authorization_response=authorization_response,
            client_secret=client_secret)

    def get_sites(self):
        r = self.__oauth.get('https://api.somfy.com/api/v1/site')
        return [Site(s) for s in r.json()]

    def get_site(self, id):
        r = self.__oauth.get('https://api.somfy.com/api/v1/site/' + id)
        return Site(r.json())

    def send_command(self, device_id, command):
        r = self.__oauth.post('https://api.somfy.com/api/v1/device/' + device_id + '/exec', json=command)
        return r.json().get('job_id')

    def get_devices(self, site_id):
        r = self.__oauth.get('https://api.somfy.com/api/v1/site/' + site_id + "/device")
        return [Device(d) for d in r.json()]

    def get_device(self, id):
        r = self.__oauth.get('https://api.somfy.com/api/v1/device/' + id)
        return Device(r.json())
