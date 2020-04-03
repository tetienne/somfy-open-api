from datetime import datetime
from enum import Enum
from typing import Optional, cast

from pymfy.api.devices.base import SomfyDevice
from pymfy.api.model import Command, Parameter


class TargetMode(Enum):
    AWAY = "away"
    AT_HOME = "at_home"
    FROST_PROTECTION = "freeze"
    MANUEL = "manual"
    SLEEP = "sleep"


class DurationType(Enum):
    FURTHER_NOTICE = "further_notice"
    NEXT_MODE = "next_mode"
    DATE = "date"


class RegulationState(Enum):
    DEROGATION = "Derogation"
    TIMETABLE = "Timetable"


class HvacState(Enum):
    HEAT = "he"
    COOL = "co"


class Thermostat(SomfyDevice):
    """Class to represent a thermostat."""

    def get_ambient_temperature(self) -> float:
        return cast(float, self.get_state("ambient_temperature"))

    def get_humidity(self) -> float:
        return cast(float, self.get_state("humidity"))

    def get_battery(self) -> int:
        return cast(int, self.get_state("battery"))

    def get_hvac_state(self) -> HvacState:
        hvac_state = self.get_state("hvac_state")
        return next((state for state in HvacState if state.value == hvac_state))

    def get_regulation_state(self) -> RegulationState:
        regulation_state = self.get_state("regulation_state")
        return next(
            (state for state in RegulationState if state.value == regulation_state)
        )

    def get_target_mode(self) -> TargetMode:
        target_mode = self.get_state("target_mode")
        return next((state for state in TargetMode if state.value == target_mode))

    def get_target_temperature(self) -> int:
        return cast(int, self.get_state("target_temperature"))

    def get_target_end_date(self) -> Optional[datetime]:
        timestamp = self.get_state("target_end_date")
        if timestamp == -1:
            return None
        return datetime.utcfromtimestamp(cast(int, timestamp))

    def get_target_start_date(self) -> Optional[datetime]:
        return datetime.utcfromtimestamp(cast(int, self.get_state("target_start_date")))

    def get_at_home_temperature(self) -> int:
        return cast(int, self.get_state("at_home_temperature"))

    def get_away_temperature(self) -> int:
        return cast(int, self.get_state("away_temperature"))

    def get_night_temperature(self) -> int:
        return cast(int, self.get_state("night_temperature"))

    def get_frost_protection_temperature(self) -> int:
        return cast(int, self.get_state("frost_protection_temperature"))

    def set_target(
        self,
        target_mode: TargetMode,
        target_temperature: int,
        duration_type: DurationType,
        duration: Optional[int] = None,
    ) -> None:
        parameters = [
            Parameter("target_mode", target_mode.value),
            Parameter("target_temperature", target_temperature),
            Parameter("duration_type", duration_type.value),
        ]
        if duration:
            parameters.append(Parameter("duration", duration))
        command = Command("set_target", parameters)
        self.send_command(command)

    def cancel_target(self) -> None:
        self.send_command(Command("cancel_target"))

    def set_at_home_temperature(self, temperature: int) -> None:
        if abs(temperature) > 999:
            raise ValueError("temperature must be between -999 and 999")
        parameter = Parameter("at_home_temperature", temperature)
        command = Command("set_at_home_temperature", parameter)
        self.send_command(command)

    def set_away_temperature(self, temperature: int) -> None:
        if abs(temperature) > 999:
            raise ValueError("temperature must be between -999 and 999")
        parameter = Parameter("away_temperature", temperature)
        command = Command("set_away_temperature", parameter)
        self.send_command(command)

    def set_night_temperature(self, temperature: int) -> None:
        if abs(temperature) > 999:
            raise ValueError("temperature must be between -999 and 999")
        parameter = Parameter("night_temperature", temperature)
        command = Command("set_night_temperature", parameter)
        self.send_command(command)

    def set_frost_protection_temperature(self, temperature: int) -> None:
        if abs(temperature) > 999:
            raise ValueError("temperature must be between -999 and 999")
        parameter = Parameter("frost_protection_temperature", temperature)
        command = Command("set_frost_protection_temperature", parameter)
        self.send_command(command)
