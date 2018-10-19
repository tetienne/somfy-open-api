from src.api.model import Device, Command, Parameter
from src.api.somfy_api import SomfyApi


class RollerShutter:
    __slots__ = 'device', 'api'

    def __init__(self, device: Device, api: SomfyApi):
        self.device = device
        self.api = api

    @property
    def position(self) -> int:
        return next((state.value for state in self.device.states if state.name == 'position')) or 0

    @position.setter
    def position(self, value: int) -> None:
        self.api.send_command(self.device.id, Command('position', Parameter('position', value)))

    def close(self) -> None:
        self.api.send_command(self.device.id, Command('close'))

    def open(self) -> None:
        self.api.send_command(self.device.id, Command('open'))

    def is_closed(self) -> bool:
        return self.position == 100
