from typing import Any

from pymfy.api.devices.base import SomfyDevice
from pymfy.api.model import Command


class CameraProtect(SomfyDevice):

    def close_shutter(self) -> None:
        self.send_command(Command('close'))

    def open_shutter(self) -> None:
        self.send_command(Command('open'))

    # Waiting documentation to know what's the type of shutter position
    def get_shutter_position(self) -> Any:
        return self.get_state('shutter_position')
