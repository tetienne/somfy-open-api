from sompy.api.model import Device
from sompy.api.somfy_api import SomfyApi


class SomfyDevice:
    __slots__ = 'device', 'api'

    def __init__(self, device: Device, api: SomfyApi):
        self.device = device
        self.api = api

    def refresh_state(self):
        self.device = self.api.get_device(self.device.id)
