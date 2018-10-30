from src.api.devices.base import SomfyDevice
from src.api.model import Command, Parameter


class RollerShutter(SomfyDevice):

    @property
    def position(self) -> int:
        return next((state.value for state in self.device.states if
                     state.name == 'position')) or 0

    @position.setter
    def position(self, value: int) -> None:
        self.api.send_command(self.device.id,
                              Command('position',
                                      Parameter('position', value)))

    def close(self) -> None:
        self.api.send_command(self.device.id, 'close')

    def open(self) -> None:
        self.api.send_command(self.device.id, 'open')

    def stop(self) -> None:
        self.api.send_command(self.device.id, 'stop')

    def identify(self) -> None:
        self.api.send_command(self.device.id, 'identify')

    def is_closed(self) -> bool:
        return self.position == 100
