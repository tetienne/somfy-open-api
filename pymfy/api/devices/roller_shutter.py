from pymfy.api.devices.base import SomfyDevice
from pymfy.api.model import Command, Parameter


class RollerShutter(SomfyDevice):

    @property
    def position(self) -> int:
        return next((state.value for state in self.device.states if
                     state.name == 'position')) or 0

    @position.setter
    def position(self, value: int) -> None:
        command = Command('position', Parameter('position', value))
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
        return self.position == 100
