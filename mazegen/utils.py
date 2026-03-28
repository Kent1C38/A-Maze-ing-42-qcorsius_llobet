from .enums import Color
from .position import Position
from sys import stdout


def bool_from_string(string: str) -> bool | None:
    """
    Used for parsing boolean values in the config file.

    This function takes the passed string, converts all uppercase letters to
    lowercase, and returns True or False depending on the result. If the string
    does not match either "True" or "False", None is returned instead.

    Args:
        string (str): The string to convert to boolean.

    Returns:
        boolean (bool): (None if the passed string does not match
        "true" or "false")
    """
    match string.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            return None


def is_pos_valid(x: int, y: int, bounds: tuple[int, int]) -> bool:
    """
    Checks whether the position x,y is in bounds.

    This function checks if x and y are within the bounds of the maze.
    It returns True if the position is within its bounds, False otherwise.

    Args:
        x (int): The X coordinate
        y (int): The Y coordinate
        bounds (tuple[int, int]): A tuple with the width and height of the
        maze.

    Returns:
        boolean (bool): True if in bounds. False otherwise.
    """
    if x not in range(0, bounds[0]):
        return False
    if y not in range(0, bounds[1]):
        return False
    return True


def get_42logo_cells(width: int, height: int) -> list[tuple[int, int]]:
    """
    Used to get the position of all the cells making the 42 logo.

    This function returns the cells making the 42 logo depending on the passed
    width and height. The cells will always be placed at the center of the
    maze. It is both used to place down the cells and send those to the
    visualizer, and to check user input when it comes to the entry and exit
    points.

    Args:
        width (int): The width of the maze.
        height (int): The height of the maze.

    Returns:
        cells (list[tuple[int, int]]): A list containing the positions of the
        cells as a tuple.
    """
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
    """
    Sets a color to a string and returns it.

    This function takes a string and adds color to it using the ANSI escape
    characters. This has been made to make colored text much easier to handle
    and work with.

    Args:
        str (str): The string to colorize.
        color (Color): The color to apply. Color is a Enum here.

    Returns:
        str (str): The colored string.
    """
    return f"\033[{color.value}m{str}\033[0m"


def bold(str: str) -> str:
    """
    Takes a string, bolds it and returns it.

    This function takes a string and makes it bold using the ANSI escape
    characters. This has been made to make this process much easier and faster.

    Args:
        str (str): The string to transform.

    Returns:
        str (str): The transformed string.
    """
    return f"\033[1m{str}\033[0m"


def move_left(amt: int) -> None:
    """
    Moves the cursor to the left X times.

    Args:
        amt (int): Move X times.

    Returns:
        None (None):
    """
    stdout.write(f"\033[{amt}D\033[0")


def move_right(amt: int) -> None:
    """
    Moves the cursor to the right X times.

    Args:
        amt (int): Move X times.

    Returns:
        None (None):
    """
    stdout.write(f"\033[{amt}C\033[0")


def move_up(amt: int) -> None:
    """
    Moves the cursor upward X times.

    Args:
        amt (int): Move X times.

    Returns:
        None (None):
    """
    stdout.write(f"\033[{amt}A\033[0")


def move_down(amt: int) -> None:
    """
    Moves the cursor downward X times.

    Args:
        amt (int): Move X times.

    Returns:
        None (None):
    """
    stdout.write(f"\033[{amt}B\033[0")


def move_to(x: int, y: int) -> None:
    """
    Moves the cursor to X and Y.

    Args:
        amt (int): Move X times.

    Returns:
        None (None):
    """
    stdout.write(f"\033[{y};{x}H\033[0")
    stdout.write("m")
