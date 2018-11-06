from typing import Tuple, List, Optional, Union

from requests_oauthlib import OAuth2Session

from sompy.api.devices.types import Category
from sompy.api.model import Command, Site, Device

BASE_URL = 'https://api.somfy.com/api/v1'

SOMFY_OAUTH = 'https://accounts.somfy.com/oauth/oauth/v2/auth'
SOMFY_TOKEN = 'https://accounts.somfy.com/oauth/oauth/v2/token'
SOMFY_REFRESH = 'https://accounts.somfy.com/oauth/oauth/v2/token'


class SomfyApi:
    __slots__ = '__oauth', '__session'

    def __init__(self, client_id: str, redirect_uri: str):
        self.__oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                                     auto_refresh_url=SOMFY_REFRESH)
        self.__session = {'client_id': client_id}

    def get_authorization_url(self) -> Tuple[str, str]:
        return self.__oauth.authorization_url(SOMFY_OAUTH)

    def request_token(self, authorization_response: str,
                      client_secret: str) -> None:

        token = self.__oauth.fetch_token(
            SOMFY_TOKEN,
            authorization_response=authorization_response,
            client_secret=client_secret)

        self.__session['oauth_token'] = token
        self.__session['client_secret'] = client_secret

    def automatic_refresh(self):
        """Refreshing an OAuth 2 token using a refresh token."""
        token = self.__session['oauth_token']

        extra = {
            'client_id': self.__session['client_id'],
            'client_secret': self.__session['client_secret'],
        }

        def token_updater(the_token):
            self.__session['oauth_token'] = the_token

        self.__oauth = OAuth2Session(self.__session['client_id'],
                                     token=token,
                                     auto_refresh_kwargs=extra,
                                     auto_refresh_url=SOMFY_REFRESH,
                                     token_updater=token_updater)

    def get_sites(self) -> List[Site]:
        r = self.__oauth.get(BASE_URL + '/site')
        return [Site(s) for s in r.json()]

    def get_site(self, site_id: str) -> Site:
        r = self.__oauth.get(BASE_URL + '/site/' + site_id)
        return Site(r.json())

    def send_command(self, device_id: str,
                     command: Union[Command, str]) -> str:
        if isinstance(command, str):
            command = Command(command)
        r = self.__oauth.post(BASE_URL + '/device/' + device_id + '/exec',
                              json=command)
        return r.json().get('job_id')

    def get_devices(self, site_id: Optional[str] = None,
                    category: Optional[Category] = None) -> List[Device]:
        site_ids = [s.id for s in self.get_sites()] if site_id is None else [
            site_id]
        devices = []
        for site_id in site_ids:
            r = self.__oauth.get(BASE_URL + '/site/' + site_id + "/device")
            devices += [Device(d) for d in r.json() if
                        category is None or category.value in Device(
                            d).categories]
        return devices

    def get_device(self, device_id) -> Device:
        r = self.__oauth.get(BASE_URL + '/device/' + device_id)
        return Device(r.json())
