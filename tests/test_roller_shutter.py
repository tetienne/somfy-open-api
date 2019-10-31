import json
import os

import httpretty
from pytest import fixture

from pymfy.api.devices.roller_shutter import RollerShutter
from pymfy.api.model import Device
from pymfy.api.somfy_api import SomfyApi, BASE_URL

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestRollerShutter:
    @fixture(scope="class")
    def device(self):
        api = SomfyApi("foo", "faa", "https://whatever.com")
        device_path = os.path.join(CURRENT_DIR, "roller_shutter.json")
        with open(device_path, "r") as get_device:
            device = Device(json.loads(get_device.read()))
        return RollerShutter(device, api)

    def test_get_position(self, device):
        assert device.get_position() == 50

    @httpretty.activate
    def test_set_position(self, device):
        url = BASE_URL + "/device/device-3/exec"
        httpretty.register_uri(httpretty.POST, url, body='{"job_id": "9"}')
        device.set_position(78)
        assert httpretty.last_request().parsed_body == {
            "name": "position",
            "parameters": [{"name": "position", "value": 78}],
        }
