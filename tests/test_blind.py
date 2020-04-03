import json
import os

import httpretty
from pytest import fixture

from pymfy.api.devices.blind import Blind
from pymfy.api.model import Device
from pymfy.api.somfy_api import BASE_URL, SomfyApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestBlind:
    @fixture(scope="class")
    def device(self):
        api = SomfyApi("foo", "faa", "https://whatever.com")
        device_path = os.path.join(CURRENT_DIR, "blind.json")
        with open(device_path, "r") as get_device:
            device = Device(**json.loads(get_device.read()))
        return Blind(device, api)

    def test_get_orientation(self, device):
        assert device.orientation == 78

    @httpretty.activate
    def test_set_orientation(self, device):
        url = BASE_URL + "/device/xxxxxx/exec"
        httpretty.register_uri(httpretty.POST, url, body='{"job_id": "9"}')
        device.orientation = 78
        assert httpretty.last_request().parsed_body == {
            "name": "rotation",
            "parameters": [{"name": "orientation", "value": 78}],
        }
