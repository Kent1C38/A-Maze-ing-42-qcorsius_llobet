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
        self.is_visited = False

    def wall_request(self, face: Facing) -> bool:
        return bool(self.__walls & face.value)

    def break_wall(self, facing: Facing) -> None:
        match facing:
            case Facing.NORTH:
                self.__walls -= Facing.NORTH.value
            case Facing.WEST:
                self.__walls -= Facing.WEST.value
            case Facing.SOUTH:
                self.__walls -= Facing.SOUTH.value
            case Facing.EAST:
                self.__walls -= Facing.EAST.value

    def get_active_walls(self) -> int:
        return self.__walls
