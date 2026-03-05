from .position import Position


def bool_from_string(string: str):
    match string.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            raise ValueError(f"Invalid boolean: {string}")


def is_pos_in_boundaries(pos: Position, width: int, height: int) -> bool:
    if pos.get_x() > width or pos.get_x() < 0:
        return False
    if pos.get_y() > height or pos.get_y() < 0:
        return False
    return True
