from src.api.devices.base import SomfyDevice


class InteriorBlind(SomfyDevice):

    def close(self) -> None:
        self.api.send_command(self.device.id, 'close')

    def open(self) -> None:
        self.api.send_command(self.device.id, 'open')

    def stop(self) -> None:
        self.api.send_command(self.device.id, 'stop')

    def identify(self) -> None:
        self.api.send_command(self.device.id, 'identify')
