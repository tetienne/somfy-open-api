import os

import httpretty
import pytest
from pytest import fixture
from requests.models import HTTPError

from pymfy.api.devices.category import Category
from pymfy.api.error import (
    AccessTokenException,
    DefinitionNotFoundException,
    DeviceNotFoundException,
    InvalidAccessTokenException,
    QuotaViolationException,
    SetupNotFoundException,
    SiteNotFoundException,
    ValidateException,
)
from pymfy.api.model import Command, Parameter
from pymfy.api.somfy_api import BASE_URL, SomfyApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSomfyApi:
    @fixture
    def api(self, request):
        params = getattr(request, "param", None) or {}
        return SomfyApi("foo", "faa", "https://whatever.com", **params)

    @httpretty.activate
    def test_get_sites(self, api):
        with open(os.path.join(CURRENT_DIR, "get_sites.json")) as get_sites:
            httpretty.register_uri(
                httpretty.GET, f"{BASE_URL}/site", body=get_sites.read()
            )
        sites = api.get_sites()
        assert len(sites) == 3
        assert sites[0].id == "site-1"
        assert sites[0].label == "TaHoma"
        assert sites[1].id == "site-2"
        assert sites[1].label == "Conexoon"

    @httpretty.activate
    def test_get_site(self, api):
        with open(os.path.join(CURRENT_DIR, "get_site.json")) as get_site:
            httpretty.register_uri(
                httpretty.GET, f"{BASE_URL}/site/site-1", body=get_site.read()
            )
        site = api.get_site("site-1")
        assert site.id == "site-1"
        assert site.label == "TaHoma"

    @httpretty.activate
    def test_devices(self, api):
        sites_path = os.path.join(CURRENT_DIR, "get_sites.json")
        devices_path_1 = os.path.join(CURRENT_DIR, "get_devices_1.json")
        devices_path_2 = os.path.join(CURRENT_DIR, "get_devices_2.json")
        with open(sites_path) as get_sites, open(devices_path_1) as get_devices_1, open(
            devices_path_2
        ) as get_devices_2:
            httpretty.register_uri(
                httpretty.GET, f"{BASE_URL}/site", body=get_sites.read()
            )
            httpretty.register_uri(
                httpretty.GET,
                f"{BASE_URL}/site/site-1/device",
                body=get_devices_1.read(),
            )
            httpretty.register_uri(
                httpretty.GET,
                f"{BASE_URL}/site/site-2/device",
                body=get_devices_2.read(),
            )

        assert len(api.get_devices("site-1")) == 3
        assert len(api.get_devices(site_id="site-1")) == 3
        assert len(api.get_devices("site-2", Category.ROLLER_SHUTTER)) == 1

    @httpretty.activate
    def test_get_device(self, api):
        device_path = os.path.join(CURRENT_DIR, "roller_shutter.json")
        with open(device_path) as get_device:
            httpretty.register_uri(
                httpretty.GET, f"{BASE_URL}/device/device-3", body=get_device.read()
            )
        device = api.get_device("device-3")
        assert device.id == "device-3"
        assert device.name == "Room 3"
        assert device.states[0].name == "position"
        assert device.states[0].value == 50
        assert device.states[0].type == "integer"

    @httpretty.activate
    def test_send_command(self, api):
        # pylint: disable=no-member
        url = f"{BASE_URL}/device/my-id/exec"
        httpretty.register_uri(httpretty.POST, url, body='{"job_id": "9"}')

        command = Command(
            "position", [Parameter("position", 10), Parameter("speed", "slow")]
        )
        assert api.send_command("my-id", command) == "9"
        assert httpretty.last_request().parsed_body == {
            "name": "position",
            "parameters": [
                {"name": "position", "value": 10},
                {"name": "speed", "value": "slow"},
            ],
        }

        command = Command("position", Parameter("position", 10))
        assert api.send_command("my-id", command) == "9"
        assert httpretty.last_request().parsed_body == {
            "name": "position",
            "parameters": [{"name": "position", "value": 10}],
        }

        command = Command("close")
        assert api.send_command("my-id", command) == "9"
        assert httpretty.last_request().parsed_body == {
            "name": "close",
            "parameters": [],
        }

        assert api.send_command("my-id", "close") == "9"
        assert httpretty.last_request().parsed_body == {
            "name": "close",
            "parameters": [],
        }

    @httpretty.activate
    @pytest.mark.parametrize(
        "api, user_agent",
        [({"user_agent": "awesome"}, "awesome"), (None, "pymfy")],
        indirect=["api"],
    )
    def test_user_agent(self, api, user_agent):
        # pylint: disable=no-member
        url = f"{BASE_URL}/device/my-id/exec"
        httpretty.register_uri(httpretty.POST, url, body='{"job_id": "9"}')
        api.send_command("my-id", "close")
        assert httpretty.last_request().headers["user-agent"] == user_agent

    @httpretty.activate
    @pytest.mark.parametrize(
        "api, error_file, exception",
        [
            (None, "access_token_expired", AccessTokenException),
            (None, "definition_not_found", DefinitionNotFoundException),
            (None, "device_not_found", DeviceNotFoundException),
            (None, "invalid_access_token", InvalidAccessTokenException),
            (None, "quota_violation", QuotaViolationException),
            (None, "setup_not_found", SetupNotFoundException),
            (None, "site_not_found", SiteNotFoundException),
            (None, "validate_error", ValidateException),
        ],
        indirect=["api"],
    )
    def test_error(self, api, error_file, exception):
        path = os.path.join(CURRENT_DIR, f"data/{error_file}.json")
        with open(path) as error:
            httpretty.register_uri(
                httpretty.GET, f"{BASE_URL}/site", body=error.read(), status=400
            )
        with pytest.raises(exception):
            api.get_sites()

    @httpretty.activate
    def test_unknown_error(self, api):
        httpretty.register_uri(httpretty.GET, f"{BASE_URL}/site", body="", status=404)
        with pytest.raises(HTTPError):
            api.get_sites()
