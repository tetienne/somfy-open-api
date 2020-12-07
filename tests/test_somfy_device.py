import json
import os

import httpretty
import pytest
from pytest import fixture

from pymfy.api.devices.base import SomfyDevice, UnsupportedCommandException
from pymfy.api.model import Command, Device
from pymfy.api.somfy_api import BASE_URL, SomfyApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSomfyDevice:
    @fixture
    def device(self):
        api = SomfyApi("foo", "faa", "https://whatever.com")
        device_path = os.path.join(CURRENT_DIR, "roller_shutter.json")
        with open(device_path) as get_device:
            dumb_device = Device(**json.loads(get_device.read()))
        return SomfyDevice(dumb_device, api)

    def test_unsupported_command(self, device):
        with pytest.raises(UnsupportedCommandException):
            device.send_command(Command("GoToTheMoon"))

    @httpretty.activate
    def test_send_command(self, device):
        url = f"{BASE_URL}/device/{device.device.id}/exec"
        httpretty.register_uri(httpretty.POST, url)
        # Exception must not be raised
        device.send_command(Command("open"))
        assert httpretty.last_request().parsed_body == {
            "name": "open",
            "parameters": [],
        }

    def test_get_state(self, device):
        assert device.get_state("position") == 50

    @httpretty.activate
    def test_refresh_state(self, device):
        device_path = os.path.join(CURRENT_DIR, "roller_shutter_2.json")
        with open(device_path) as get_device:
            httpretty.register_uri(
                httpretty.GET, f"{BASE_URL}/device/device-3", body=get_device.read()
            )
        device.refresh_state()
        assert device.get_state("position") == 70
