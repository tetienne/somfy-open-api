from enum import Enum, unique


@unique
class Category(Enum):
    ROLLER_SHUTTER = "roller_shutter"
    HUB = "hub"
    INTERIOR_BLIND = "interior_blind"
    EXTERIOR_BLIND = "exterior_blind"
    CAMERA = "camera"
