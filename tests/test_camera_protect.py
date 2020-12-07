import json
import os

import httpretty
from pytest import fixture

from pymfy.api.devices.camera_protect import CameraProtect
from pymfy.api.model import Device
from pymfy.api.somfy_api import BASE_URL, SomfyApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCameraProtect:
    @fixture(scope="class")
    def device(self):
        api = SomfyApi("foo", "faa", "https://whatever.com")
        device_path = os.path.join(CURRENT_DIR, "camera.json")
        with open(device_path) as get_device:
            device = Device(**json.loads(get_device.read()))
        return CameraProtect(device, api)

    @httpretty.activate
    def test_open_shutter(self, device):
        url = f"{BASE_URL}/device/device-9/exec"
        httpretty.register_uri(httpretty.POST, url, body='{"job_id": "9"}')
        device.open_shutter()
        assert httpretty.last_request().parsed_body == {  # pylint: disable=no-member
            "name": "shutter_open",
            "parameters": [],
        }

    @httpretty.activate
    def test_close_shutter(self, device):
        url = f"{BASE_URL}/device/device-9/exec"
        httpretty.register_uri(httpretty.POST, url, body='{"job_id": "9"}')
        device.close_shutter()
        assert httpretty.last_request().parsed_body == {  # pylint: disable=no-member
            "name": "shutter_close",
            "parameters": [],
        }

    def test_get_shutter_position(self, device):
        assert device.get_shutter_position() == "opened"
