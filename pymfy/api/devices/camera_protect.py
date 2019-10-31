from typing import Any

from pymfy.api.devices.base import SomfyDevice
from pymfy.api.model import Command


class CameraProtect(SomfyDevice):
    """Class to represent a camera"""

    def close_shutter(self) -> None:
        self.send_command(Command("close"))

    def open_shutter(self) -> None:
        self.send_command(Command("open"))

    # TODO Waiting documentation to know what's the returned type
    def get_shutter_position(self) -> Any:
        return self.get_state("shutter_position")
