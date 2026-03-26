from .enums import Color
from .position import Position
from sys import stdout


def bool_from_string(string: str):
    match string.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            return None


def is_pos_valid(x: int, y: int, bounds: tuple[int, int]) -> bool:
    if x not in range(0, bounds[0]):
        return False
    if y not in range(0, bounds[1]):
        return False
    return True


def get_42logo_cells(width: int, height: int) -> list[tuple[int, int]]:
    x_center = width // 2
    y_center = height // 2
    start = Position(x=x_center - 3, y=y_center - 2)
    return [(start.x, start.y),
            (start.x, start.y + 1),
            (start.x, start.y + 2),
            (start.x + 1, start.y + 2),
            (start.x + 2, start.y + 2),
            (start.x + 2, start.y + 3),
            (start.x + 2, start.y + 4),

            (start.x + 4, start.y),
            (start.x + 5, start.y),
            (start.x + 6, start.y),
            (start.x + 6, start.y + 1),
            (start.x + 6, start.y + 2),
            (start.x + 5, start.y + 2),
            (start.x + 4, start.y + 2),
            (start.x + 4, start.y + 3),
            (start.x + 4, start.y + 4),
            (start.x + 5, start.y + 4),
            (start.x + 6, start.y + 4)]


def colorize(str: str, color: Color) -> str:
    return f"\033[{color.value}m{str}\033[0m"


def bold(str: str) -> str:
    return f"\033[1m{str}\033[0m"


def move_left(amt: int) -> None:
    stdout.write(f"\033[{amt}D\033[0")


def move_right(amt: int) -> None:
    stdout.write(f"\033[{amt}C\033[0")


def move_up(amt: int) -> None:
    stdout.write(f"\033[{amt}A\033[0")


def move_down(amt: int) -> None:
    stdout.write(f"\033[{amt}B\033[0")
