import json
import os

import pytest

from pymfy.api.devices.base import SomfyDevice, UnsupportedCommandException
from pymfy.api.model import Device, Command
from pymfy.api.somfy_api import SomfyApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSomfyDevice:
    __slots__ = 'api'

    def setup_method(self):
        self.api = SomfyApi('foo', 'faa')

    def test_unsupported_command(self):
        device_path = os.path.join(CURRENT_DIR, 'get_device.json')
        with open(device_path, 'r') as get_device:
            dumb_device = Device(json.loads(get_device.read()))
        somfy_device = SomfyDevice(dumb_device, self.api)
        with pytest.raises(UnsupportedCommandException):
            somfy_device.send_command(Command('GoToTheMoon'))
