from typing import Any, Dict


class ServerException(Exception):
    def __init__(self, response: Dict[str, Any]) -> None:
        self.error_code = response["fault"]["detail"]["errorcode"]
        self.fault_string = response["fault"]["faultstring"]
        super().__init__()

    def __str__(self) -> str:
        return f"error_code: {self.error_code}, fault_string: {self.fault_string}"


class InvalidAccessTokenException(ServerException):
    pass


class QuotaViolationException(ServerException):
    pass


class AccessTokenException(ServerException):
    pass


class ClientException(Exception):
    def __init__(self, response: Dict[str, Any]) -> None:
        self.data = response["data"]
        self.message = response["message"]
        super().__init__()

    def __str__(self) -> str:
        return f"message: {self.message}, data: {self.data}"


class ValidateException(ClientException):
    pass


class DeviceNotFoundException(ClientException):
    pass


class DefinitionNotFoundException(ClientException):
    pass


class SiteNotFoundException(ClientException):
    pass


class SetupNotFoundException(ClientException):
    pass


SERVER_ERROR = {
    "oauth.v2.InvalidAccessToken": InvalidAccessTokenException,
    "keymanagement.service.access_token_expired": AccessTokenException,
    "policies.ratelimit.QuotaViolation": QuotaViolationException,
}

CLIENT_ERROR = {
    "ValidateError": ValidateException,
    "device_not_found": DeviceNotFoundException,
    "definition_not_found": DefinitionNotFoundException,
    "setup_not_found": SetupNotFoundException,
    "site_not_found": SiteNotFoundException,
}
