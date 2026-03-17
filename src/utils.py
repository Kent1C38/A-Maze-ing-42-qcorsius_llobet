from enums import Color


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


def colorize(str: str, color: Color) -> str:
    return f"\033[{color.value}m{str}\033[0m"


def bold(str: str) -> str:
    return f"\033[1m{str}\033[0m"
