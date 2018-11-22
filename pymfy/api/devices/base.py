from typing import Union

from pymfy.api.model import Device, Command
from pymfy.api.somfy_api import SomfyApi


class SomfyDevice:
    __slots__ = 'device', 'api'

    def __init__(self, device: Device, api: SomfyApi):
        self.device = device
        self.api = api

    def refresh_state(self) -> None:
        self.device = self.api.get_device(self.device.id)

    def send_command(self, command: Command) -> None:
        if command.name in self.device.capabilities:
            self.api.send_command(self.device.id, command)
        else:
            message_template = 'Command {} not available. ' \
                               'Categories: {}, Type: {}, Capabilities: {}'
            message = message_template.format(command.name,
                                              self.device.categories,
                                              self.device.type,
                                              self.device.capabilities)
            raise UnsupportedCommandException(message)

    def get_state(self, state_name) -> Union[str, int]:
        return next((state.value for state in self.device.states if
                     state.name == state_name))


class UnsupportedCommandException(Exception):
    """Raise a Command is not listed in the capabilities of a device."""
