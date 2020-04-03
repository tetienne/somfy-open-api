import os

import httpretty
from pytest import fixture

from pymfy.api.devices.category import Category
from pymfy.api.model import Command, Parameter
from pymfy.api.somfy_api import BASE_URL, SomfyApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSomfyApi:
    @fixture
    def api(self):
        return SomfyApi("foo", "faa", "https://whatever.com")

    @httpretty.activate
    def test_get_sites(self, api):
        with open(os.path.join(CURRENT_DIR, "get_sites.json"), "r") as get_sites:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/site", body=get_sites.read()
            )
        sites = api.get_sites()
        assert len(sites) == 2
        assert sites[0].id == "site-1"
        assert sites[0].label == "TaHoma"
        assert sites[1].id == "site-2"
        assert sites[1].label == "Conexoon"

    @httpretty.activate
    def test_get_site(self, api):
        with open(os.path.join(CURRENT_DIR, "get_site.json"), "r") as get_site:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/site/site-1", body=get_site.read()
            )
        site = api.get_site("site-1")
        assert site.id == "site-1"
        assert site.label == "TaHoma"

    @httpretty.activate
    def test_devices(self, api):
        sites_path = os.path.join(CURRENT_DIR, "get_sites.json")
        devices_path_1 = os.path.join(CURRENT_DIR, "get_devices_1.json")
        devices_path_2 = os.path.join(CURRENT_DIR, "get_devices_2.json")
        with open(sites_path, "r") as get_sites, open(
            devices_path_1, "r"
        ) as get_devices_1, open(devices_path_2, "r") as get_devices_2:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/site", body=get_sites.read()
            )
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/site/site-1/device",
                body=get_devices_1.read(),
            )
            httpretty.register_uri(
                httpretty.GET,
                BASE_URL + "/site/site-2/device",
                body=get_devices_2.read(),
            )

        assert len(api.get_devices()) == 4
        assert len(api.get_devices("site-1")) == 3
        assert len(api.get_devices(site_id="site-1")) == 3
        assert len(api.get_devices(category=Category.ROLLER_SHUTTER)) == 3
        assert len(api.get_devices("site-2", Category.ROLLER_SHUTTER)) == 1

    @httpretty.activate
    def test_get_device(self, api):
        device_path = os.path.join(CURRENT_DIR, "roller_shutter.json")
        with open(device_path, "r") as get_device:
            httpretty.register_uri(
                httpretty.GET, BASE_URL + "/device/device-3", body=get_device.read()
            )
        device = api.get_device("device-3")
        assert device.id == "device-3"
        assert device.name == "Room 3"
        assert device.states[0].name == "position"
        assert device.states[0].value == 50
        assert device.states[0].type == "integer"

    @httpretty.activate
    def test_send_command(self, api):
        url = BASE_URL + "/device/my-id/exec"
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
