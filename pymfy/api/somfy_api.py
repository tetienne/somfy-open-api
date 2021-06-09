from json import JSONDecodeError
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from oauthlib.oauth2 import TokenExpiredError
from requests import Response
from requests_oauthlib import OAuth2Session

from pymfy.api.devices.category import Category
from pymfy.api.error import CLIENT_ERROR, SERVER_ERROR, ClientException, ServerException
from pymfy.api.model import Command, Device, Site

BASE_URL = "https://api.somfy.com/api/v1"

SOMFY_OAUTH = "https://accounts.somfy.com/oauth/oauth/v2/auth"
SOMFY_TOKEN = "https://accounts.somfy.com/oauth/oauth/v2/token"
SOMFY_REFRESH = "https://accounts.somfy.com/oauth/oauth/v2/token"


class SomfyApi:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[str] = None,
        token: Optional[Dict[str, str]] = None,
        token_updater: Optional[Callable[[str], None]] = None,
        user_agent: Optional[str] = "pymfy",
    ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.token_updater = token_updater

        extra = {"client_id": self.client_id, "client_secret": self.client_secret}

        self._oauth = OAuth2Session(
            client_id=client_id,
            token=token,
            redirect_uri=redirect_uri,
            auto_refresh_kwargs=extra,
            token_updater=token_updater,
        )
        self._oauth.headers["User-Agent"] = user_agent

    def get_sites(self) -> List[Site]:
        response = self.get("/site")
        response.raise_for_status()
        return [Site(**s) for s in response.json()]

    def get_site(self, site_id: str) -> Site:
        response = self.get(f"/site/{site_id}")
        response.raise_for_status()
        return Site(**response.json())

    def send_command(self, device_id: str, command: Union[Command, str]) -> str:
        if isinstance(command, str):
            command = Command(command)
        response = self.post(f"/device/{device_id}/exec", json=command)
        response.raise_for_status()
        return response.json().get("job_id")

    def get_devices(
        self, site_id: str, category: Optional[Category] = None
    ) -> List[Device]:
        response = self.get(f"/site/{site_id}/device")
        try:
            content = response.json()
        except JSONDecodeError:
            response.raise_for_status()

        devices = [
            Device(**d)
            for d in content
            if category is None or category.value in Device(**d).categories
        ]
        return devices

    def get_device(self, device_id: str) -> Device:
        response = self.get(f"/device/{device_id}")
        response.raise_for_status()
        return Device(**response.json())

    def get(self, path: str) -> Response:
        """Fetch a URL from the Somfy API."""
        return self._request("get", path)

    def post(self, path: str, *, json: Dict[str, Any]) -> Response:
        """Post data to the Somfy API."""
        return self._request("post", path, json=json)

    def get_authorization_url(self, state: Optional[str] = None) -> Tuple[str, str]:
        return self._oauth.authorization_url(SOMFY_OAUTH, state)

    def request_token(
        self, authorization_response: Optional[str] = None, code: Optional[str] = None
    ) -> Dict[str, str]:
        """Generic method for fetching a Somfy access token.

        :param authorization_response: Authorization response URL, the callback
                                       URL of the request back to you.
        :param code: Authorization code
        :return: A token dict
        """
        return self._oauth.fetch_token(
            SOMFY_TOKEN,
            authorization_response=authorization_response,
            code=code,
            client_secret=self.client_secret,
        )

    def refresh_tokens(self) -> Dict[str, Union[str, int]]:
        """Refresh and return new Somfy tokens."""
        token = self._oauth.refresh_token(SOMFY_REFRESH)

        if self.token_updater is not None:
            self.token_updater(token)

        return token

    def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Make a request.

        We don't use the built-in token refresh mechanism of OAuth2 session because
        we want to allow overriding the token refresh logic.
        """
        url = f"{BASE_URL}{path}"
        try:
            response = getattr(self._oauth, method)(url, **kwargs)
        except TokenExpiredError:
            self._oauth.token = self.refresh_tokens()

            response = getattr(self._oauth, method)(url, **kwargs)

        self._check_response(response)
        return response

    def _check_response(self, response: Response) -> None:
        """Check response does not contain any error."""
        if response.status_code == 200:
            return
        error = response.json()
        if "fault" in error:
            error_code = error["fault"]["detail"]["errorcode"]
            raise SERVER_ERROR.get(error_code, ServerException)(error)
        if "message" in error:
            message = error["message"]
            raise CLIENT_ERROR.get(message, ClientException)(error)
        response.raise_for_status()
