from enum import Enum


class Facing(Enum):
    NORTH = 0b1000
    EAST = 0b0100
    SOUTH = 0b0010
    WEST = 0b0001


class Cell:
    def __init__(self, north: bool, east: bool,
                 south: bool, west: bool):
        value = 0b0000
        if north:
            value = value + Facing.NORTH.value
        if east:
            value = value + Facing.EAST.value
        if south:
            value = value + Facing.SOUTH.value
        if west:
            value = value + Facing.WEST.value

        self.__walls = value

    def wall_request(self, face: Facing) -> bool:
        match face:
            case Facing.NORTH:
                return self.__walls & Facing.NORTH.value == Facing.NORTH.value

            case Facing.EAST:
                return self.__walls & Facing.EAST.value == Facing.EAST.value

            case Facing.SOUTH:
                return self.__walls & Facing.SOUTH.value == Facing.SOUTH.value

            case Facing.WEST:
                return self.__walls & Facing.WEST.value == Facing.WEST.value

    def get_active_walls(self) -> int:
        return self.__walls
