from enum import Enum, unique


@unique
class Category(Enum):
    ROLLER_SHUTTER = 'roller_shutter'
    HUB = 'hub'
