from enum import Enum


class Facing(Enum):
    NORTH = (0b0001, (0, -1))
    EAST = (0b0010, (1, 0))
    SOUTH = (0b0100, (0, 1))
    WEST = (0b1000, (-1, 0))

    @property
    def bin_value(self) -> int:
        return self.value[0]

    @property
    def dx(self) -> int:
        return self.value[1][0]

    @property
    def dy(self) -> int:
        return self.value[1][1]

    @property
    def vector(self) -> tuple[int, int]:
        return self.value[1]


class Cell:
    def __init__(self) -> None:
        self.__walls = 0b1111
        self.is_visited = False
        self.is_unbreakable = False

    def set_unbreakable(self, is_unbreakable: bool) -> None:
        self.is_unbreakable = is_unbreakable

    def wall_request(self, face: Facing) -> bool:
        return bool(self.__walls & face.bin_value)

    def break_wall(self, facing: Facing) -> None:
        self.__walls -= facing.bin_value

    def get_active_walls(self) -> int:
        return self.__walls

    def reset(self) -> None:
        self.__walls = 0b1111
        self.is_visited = False
        self.is_unbreakable = False
