from pymfy.api.devices.roller_shutter import RollerShutter
from pymfy.api.model import Command, Parameter


class Blind(RollerShutter):
    """Class to represent a blind."""

    @property
    def orientation(self) -> int:
        return self.get_state("orientation")

    @orientation.setter
    def orientation(self, value: int) -> None:
        command = Command("rotation", Parameter("orientation", value))
        self.send_command(command)
