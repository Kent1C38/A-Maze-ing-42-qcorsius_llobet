from enum import Enum


class Facing(Enum):
    NORTH = (0b1000, (0, -1))
    EAST = (0b0100, (1, 0))
    SOUTH = (0b0010, (0, 1))
    WEST = (0b0001, (-1, 0))

    @property
    def dx(self):
        return self.value[1][0]

    @property
    def dy(self):
        return self.value[1][1]


class Cell:
    def __init__(self, north: bool, east: bool,
                 south: bool, west: bool):
        value = 0b0000
        if north:
            value = value + Facing.NORTH.value[0]
        if east:
            value = value + Facing.EAST.value[0]
        if south:
            value = value + Facing.SOUTH.value[0]
        if west:
            value = value + Facing.WEST.value[0]

        self.__walls = value
        self.is_visited = False

    def wall_request(self, face: Facing) -> bool:
        return bool(self.__walls & face.value[0])

    def break_wall(self, facing: Facing) -> None:
        match facing:
            case Facing.NORTH:
                self.__walls -= Facing.NORTH.value[0]
            case Facing.WEST:
                self.__walls -= Facing.WEST.value[0]
            case Facing.SOUTH:
                self.__walls -= Facing.SOUTH.value[0]
            case Facing.EAST:
                self.__walls -= Facing.EAST.value[0]

    def get_active_walls(self) -> int:
        return self.__walls
