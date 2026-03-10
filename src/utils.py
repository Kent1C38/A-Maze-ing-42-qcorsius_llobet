from enum import Enum


def bool_from_string(string: str):
    match string.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            raise ValueError(f"Invalid boolean: {string}")


def is_pos_valid(x: int, y: int, bounds: tuple[int, int]) -> bool:
    if x not in range(0, bounds[0]):
        return False
    if y not in range(0, bounds[1]):
        return False
    return True


class Direction(Enum):
    NORTH = (0, -1),
    EAST = (1, 0),
    SOUTH = (0, 1),
    WEST = (-1, 0)

    @property
    def dx(self):
        return self.value[0]

    @property
    def dy(self):
        return self.value[1]
