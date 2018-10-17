from requests_oauthlib import OAuth2Session

SOMFY_OAUTH = 'https://accounts.somfy.com/oauth/oauth/v2/auth'
SOMFY_TOKEN = 'https://accounts.somfy.com/oauth/oauth/v2/token'
SOMFY_REFRESH = 'https://accounts.somfy.com/oauth/oauth/v2/token'


class SomfyApi:
    __slots__ = '__oauth'

    def __init__(self, client_id, redirect_uri):
        self.__oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, auto_refresh_url=SOMFY_REFRESH)

    def set_bearer_token(token):
        pass

    def set_somfy_credentials(client_id, client_secret, access_token, refresh_token):
        pass

    def refresh_access_token(self):
        pass

    def get_authorization_url(self):
        return self.__oauth.authorization_url(SOMFY_OAUTH)

    def request_token(self, authorization_response, client_secret):
        return self.__oauth.fetch_token(
            SOMFY_TOKEN,
            authorization_response=authorization_response,
            client_secret=client_secret)

    def get_sites(self):
        return self.__oauth.get('https://api.somfy.com/api/v1/site')

    def get_site(self, id):
        pass

    def send_command(self, device_id):
        pass

    def get_devices(self, site_id):
        pass

    def get_device(self, device_id):
        pass
