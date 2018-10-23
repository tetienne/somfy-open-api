from typing import Tuple, List

from requests_oauthlib import OAuth2Session

from src.api.model import Device, Command
from src.api.model import Site

BASE_URL = 'https://api.somfy.com/api/v1'

SOMFY_OAUTH = 'https://accounts.somfy.com/oauth/oauth/v2/auth'
SOMFY_TOKEN = 'https://accounts.somfy.com/oauth/oauth/v2/token'
SOMFY_REFRESH = 'https://accounts.somfy.com/oauth/oauth/v2/token'


class SomfyApi:
    __slots__ = '__oauth'

    def __init__(self, client_id: str, redirect_uri: str):
        self.__oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, auto_refresh_url=SOMFY_REFRESH)

    def get_authorization_url(self) -> Tuple[str, str]:
        return self.__oauth.authorization_url(SOMFY_OAUTH)

    def request_token(self, authorization_response: str, client_secret: str) -> None:
        self.__oauth.fetch_token(
            SOMFY_TOKEN,
            authorization_response=authorization_response,
            client_secret=client_secret)

    def get_sites(self) -> List[Site]:
        r = self.__oauth.get(BASE_URL + '/site')
        return [Site(s) for s in r.json()]

    def get_site(self, site_id: str) -> Site:
        r = self.__oauth.get(BASE_URL + '/site/' + site_id)
        return Site(r.json())

    def send_command(self, device_id: str, command: Command) -> str:
        r = self.__oauth.post(BASE_URL + '/device/' + device_id + '/exec', json=command)
        return r.json().get('job_id')

    def get_devices(self, site_id: str) -> List[Device]:
        r = self.__oauth.get(BASE_URL + '/site/' + site_id + "/device")
        return [Device(d) for d in r.json()]

    def get_device(self, device_id) -> Device:
        r = self.__oauth.get(BASE_URL + '/device/' + device_id)
        return Device(r.json())
