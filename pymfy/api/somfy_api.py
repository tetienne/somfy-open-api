import json
from typing import Tuple, List, Optional, Union

from requests_oauthlib import OAuth2Session

from pymfy.api.devices.category import Category
from pymfy.api.model import Command, Site, Device

BASE_URL = 'https://api.somfy.com/api/v1'

SOMFY_OAUTH = 'https://accounts.somfy.com/oauth/oauth/v2/auth'
SOMFY_TOKEN = 'https://accounts.somfy.com/oauth/oauth/v2/token'
SOMFY_REFRESH = 'https://accounts.somfy.com/oauth/oauth/v2/token'


class SomfyApi:
    __slots__ = '_oauth', 'client_id', 'client_secret', 'cache_path', '_token'

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str,
                 cache_path: str = None):

        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_path = cache_path
        self.token = None

        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        def token_setter(token):
            self.token = token

        self._oauth = OAuth2Session(client_id=client_id,
                                    token=self.token,
                                    redirect_uri=redirect_uri,
                                    auto_refresh_kwargs=extra,
                                    auto_refresh_url=SOMFY_REFRESH,
                                    token_updater=token_setter)

    def get_authorization_url(self) -> Tuple[str, str]:
        return self._oauth.authorization_url(SOMFY_OAUTH)

    def request_token(self, authorization_response: str) -> None:
        self.token = self._oauth.fetch_token(
            SOMFY_TOKEN,
            authorization_response=authorization_response,
            client_secret=self.client_secret)

    @property
    def token(self) -> str:
        token = self._token
        if self.cache_path:
            try:
                with open(self.cache_path, 'r') as cache:
                    token = json.loads(cache.read())
            except IOError:
                pass
        return token

    @token.setter
    def token(self, token: str) -> None:
        self._token = token
        if self.cache_path and token:
            with open(self.cache_path, 'w') as cache:
                cache.write(json.dumps(token))

    def get_sites(self) -> List[Site]:
        r = self._oauth.get(BASE_URL + '/site')
        r.raise_for_status()
        return [Site(s) for s in r.json()]

    def get_site(self, site_id: str) -> Site:
        r = self._oauth.get(BASE_URL + '/site/' + site_id)
        r.raise_for_status()
        return Site(r.json())

    def send_command(self, device_id: str,
                     command: Union[Command, str]) -> str:
        if isinstance(command, str):
            command = Command(command)
        r = self._oauth.post(BASE_URL + '/device/' + device_id + '/exec',
                             json=command)
        r.raise_for_status()
        return r.json().get('job_id')

    def get_devices(self, site_id: Optional[str] = None,
                    category: Optional[Category] = None) -> List[Device]:
        site_ids = [s.id for s in self.get_sites()] if site_id is None else [
            site_id]
        devices = []
        for site_id in site_ids:
            r = self._oauth.get(BASE_URL + '/site/' + site_id + "/device")
            r.raise_for_status()
            devices += [Device(d) for d in r.json() if
                        category is None or category.value in Device(
                            d).categories]
        return devices

    def get_device(self, device_id: str) -> Device:
        r = self._oauth.get(BASE_URL + '/device/' + device_id)
        r.raise_for_status()
        return Device(r.json())
