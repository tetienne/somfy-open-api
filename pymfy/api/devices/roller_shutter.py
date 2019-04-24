from typing import Optional

from pymfy.api.devices.base import SomfyDevice
from pymfy.api.model import Command, Parameter


class RollerShutter(SomfyDevice):
    """Class to represent a roller shutter."""

    def get_position(self) -> int:
        return self.get_state('position')

    def set_position(self, value: int,
                     low_speed: Optional[int] = False) -> None:
        command_name = 'position_low_speed' if low_speed else 'position'
        command = Command(command_name, Parameter('position', value))
        self.send_command(command)

    def close(self) -> None:
        self.send_command(Command('close'))

    def open(self) -> None:
        self.send_command(Command('open'))

    def stop(self) -> None:
        self.send_command(Command('stop'))

    def identify(self) -> None:
        self.send_command(Command('identify'))

    def is_closed(self) -> bool:
        return self.get_position() == 100
