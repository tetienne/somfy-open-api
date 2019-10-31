import json
import os

import httpretty
import pytest

from pymfy.api.devices.base import SomfyDevice, UnsupportedCommandException
from pymfy.api.model import Device, Command
from pymfy.api.somfy_api import SomfyApi, BASE_URL

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSomfyDevice:
    __slots__ = "api", "dumb_device", "somfy_device"

    def setup_method(self):
        self.api = SomfyApi("foo", "faa", "https://whatever.com")
        device_path = os.path.join(CURRENT_DIR, "roller_shutter.json")
        with open(device_path, "r") as get_device:
            self.dumb_device = Device(json.loads(get_device.read()))
        self.somfy_device = SomfyDevice(self.dumb_device, self.api)

    @httpretty.activate
    def test_unsupported_command(self):
        with pytest.raises(UnsupportedCommandException):
            self.somfy_device.send_command(Command("GoToTheMoon"))

    @httpretty.activate
    def test_send_command(self):
        url = BASE_URL + "/device/" + self.dumb_device.id + "/exec"
        httpretty.register_uri(httpretty.POST, url)
        # Exception must not be raised
        self.somfy_device.send_command(Command("open"))
