import json
import os
from datetime import datetime

import httpretty
from pytest import fixture

from pymfy.api.devices.thermostat import Thermostat
from pymfy.api.model import Device
from pymfy.api.somfy_api import SomfyApi, BASE_URL

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

URL = BASE_URL + "/device/device-99/exec"


@httpretty.activate
class TestThermostat:
    @fixture(scope="class")
    def device(self):
        api = SomfyApi("foo", "faa", "https://whatever.com")
        device_path = os.path.join(CURRENT_DIR, "hvac.json")
        with open(device_path, "r") as get_device:
            device = Device(**json.loads(get_device.read()))
        return Thermostat(device, api)

    def test_get_ambient_temperature(self, device):
        assert device.get_ambient_temperature() == 23.3

    def test_get_humidity(self, device):
        assert device.get_humidity() == 40

    def test_get_battery(self, device):
        assert device.get_battery() == 93

    def test_get_hvac_state(self, device):
        assert device.get_hvac_state() == "he"

    def test_get_regulation_state(self, device):
        assert device.get_regulation_state() == "Derogation"

    def test_get_target_mode(self, device):
        assert device.get_target_mode() == "at_home"

    def test_get_target_get_temperature(self, device):
        assert device.get_target_temperature() == 18

    def test_get_target_end_date(self, device):
        assert device.get_target_end_date() == datetime(2018, 11, 20, 19, 26, 2)

    def test_get_target_start_date(self, device):
        assert device.get_target_start_date() == datetime(2018, 11, 20, 17, 26, 2)

    def test_get_at_home_temperature(self, device):
        assert device.get_at_home_temperature() == 18

    def test_get_away_temperature(self, device):
        assert device.get_away_temperature() == 15

    def test_get_night_temperature(self, device):
        assert device.get_night_temperature() == 15

    def test_get_frost_protection_temperature(self, device):
        assert device.get_frost_protection_temperature() == 8

    def test_set_target(self, device):
        httpretty.register_uri(httpretty.POST, URL, body='{"job_id": "9"}')
        device.set_target("at_home", 18, 10, "h")
        assert httpretty.last_request().parsed_body == {
            "name": "set_target",
            "parameters": [
                {"name": "target_mode", "value": "at_home"},
                {"name": "target_temperature", "value": 18},
                {"name": "duration", "value": 10},
                {"name": "duration_type", "value": "h"},
            ],
        }

    def test_cancel_target(self, device):
        httpretty.register_uri(httpretty.POST, URL, body='{"job_id": "9"}')
        device.cancel_target()
        assert httpretty.last_request().parsed_body == {
            "name": "cancel_target",
            "parameters": [],
        }

    def test_set_at_home_temperature(self, device):
        httpretty.register_uri(httpretty.POST, URL, body='{"job_id": "9"}')
        device.set_at_home_temperature(10)
        assert httpretty.last_request().parsed_body == {
            "name": "set_at_home_temperature",
            "parameters": [{"name": "at_home_temperature", "value": 10}],
        }

    def test_set_away_temperature(self, device):
        httpretty.register_uri(httpretty.POST, URL, body='{"job_id": "9"}')
        device.set_away_temperature(12)
        assert httpretty.last_request().parsed_body == {
            "name": "set_away_temperature",
            "parameters": [{"name": "away_temperature", "value": 12}],
        }

    def test_set_night_temperature(self, device):
        httpretty.register_uri(httpretty.POST, URL, body='{"job_id": "9"}')
        device.set_night_temperature(13)
        assert httpretty.last_request().parsed_body == {
            "name": "set_night_temperature",
            "parameters": [{"name": "night_temperature", "value": 13}],
        }

    def test_set_frost_protection_temperature(self, device):
        httpretty.register_uri(httpretty.POST, URL, body='{"job_id": "9"}')
        device.set_frost_protection_temperature(8)
        assert httpretty.last_request().parsed_body == {
            "name": "set_frost_protection_temperature",
            "parameters": [{"name": "frost_protection_temperature", "value": 8}],
        }
