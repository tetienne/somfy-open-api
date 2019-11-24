from typing import cast

from pymfy.api.devices.base import SomfyDevice
from pymfy.api.model import Command


class CameraProtect(SomfyDevice):
    """Class to represent a camera"""

    def close_shutter(self) -> None:
        self.send_command(Command("shutter_close"))

    def open_shutter(self) -> None:
        self.send_command(Command("shutter_open"))

    def get_shutter_position(self) -> str:
        """ Possible returned values are opened and closed """
        return cast(str, self.get_state("shutter_position"))
