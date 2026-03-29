#!/usr/bin/python3.10

# --- IMPORTS -----------------------------------------------------------------

from typing import Dict, List
from time import sleep

from .menus import (BaseMenu, MainMenu, ColorMenu, DisplayMenu, AnimMenu,
                    OptionsMenu, MazeMenu)
from ..utils import colorize, bold, move_up, move_right
from ..enums import Color

# --- EXCEPTIONS --------------------------------------------------------------


class MenuNotFoundError(BaseException):
    """
    The MenuNotFoundError.

    Inherits from BaseException. It is only raised when the InputHandler
    cannot find the requested menu.
    """
    def __init__(self, menu: str) -> None:
        """
        Raises a MenuNotFoundError.

        Used when a requested menu canont be found.

        Args:
            menu (str): The requested menu.

        Returns:
            none (None):
        """
        super().__init__(f"Cannot go to menu \"{menu}\"")

# --- CLASSES -----------------------------------------------------------------


class InputHandler:
    """
    The InputHandler class.

    It contains all logic related to user input. It should not be instantiated
    as its own object.
    """
    __menus: Dict[str, BaseMenu] = {
        "Main": MainMenu("Main Menu", [
            f"1 ║ {colorize('GENERATE MAZE', Color.WHITE)}",
            f"2 ║ {colorize('SOLVE MAZE', Color.WHITE)}",
            f"3 ║ {colorize('ERASE MAZE', Color.YELLOW)}",
            f"4 ║ {colorize('OPTIONS', Color.WHITE)}",
            f"0 ║ {colorize('EXIT', Color.RED)}",
        ]),
        "Color": ColorMenu("Color Menu", [
            f"1 ║ {colorize('GRAY', Color.DARK_GRAY)}",
            f"2 ║ {colorize('RED', Color.RED)}",
            f"3 ║ {colorize('GREEN', Color.GREEN)}",
            f"4 ║ {colorize('YELLOW', Color.YELLOW)}",
            f"5 ║ {colorize('BLUE', Color.BLUE)}",
            f"6 ║ {colorize('PURPLE', Color.PURPLE)}",
            f"7 ║ {colorize('CYAN', Color.CYAN)}",
            f"8 ║ {colorize('WHITE', Color.WHITE)}",
            f"0 ║ {colorize('GO BACK', Color.RED)}",
        ]),
        "Animation": AnimMenu("Animation Menu", [
            f"1 ║ {colorize('MAZE ANIMATION', Color.RED)}",
            f"2 ║ {colorize('PATH ANIMATION', Color.RED)}",
            f"0 ║ {colorize('GO BACK', Color.RED)}",
        ]),
        "Display": DisplayMenu("Color Menu", [
            f"1 ║ {colorize('WALLS', Color.WHITE)}",
            f"2 ║ {colorize('PATH', Color.WHITE)}",
            f"3 ║ {colorize('ENTRY', Color.WHITE)}",
            f"4 ║ {colorize('EXIT', Color.WHITE)}",
            f"5 ║ {colorize('42 LOGO', Color.WHITE)}",
            f"0 ║ {colorize('GO BACK', Color.RED)}",
        ]),
        "Options": OptionsMenu("Options Menu", [
            f"1 ║ {colorize('MAZE CONFIGURATION', Color.WHITE)}",
            f"2 ║ {colorize('COLOR OPTIONS', Color.WHITE)}",
            f"3 ║ {colorize('ANIMATION OPTIONS', Color.WHITE)}",
            f"0 ║ {colorize('GO BACK', Color.RED)}",
        ]),
        "Maze": MazeMenu("Maze Config", [
            f"1 ║ {colorize('WIDTH: 20', Color.WHITE)}",
            f"2 ║ {colorize('HEIGHT: 15', Color.WHITE)}",
            f"3 ║ {colorize('ENTRY: [5, 4]', Color.WHITE)}",
            f"4 ║ {colorize('EXIT: [19, 14]', Color.WHITE)}",
            f"5 ║ {colorize('PERFECT', Color.WHITE)}",
            f"6 ║ {colorize('SEED: 7852486468', Color.WHITE)}",
            f"0 ║ {colorize('GO BACK', Color.RED)}",
        ])
    }
    __opened: BaseMenu | None = __menus.get("Main")

    @classmethod
    def goto(cls, menu: str) -> None:
        """
        Goes to a menu.

        If the requested menu is found, sets that menu to be the active one.
        Otherwise raises a MenuNotFoundError.

        Args:
            menu (str): The menu to go to.

        Returns:
            none (None):

        Raises:
            MenuNotFoundError
        """
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        m: BaseMenu | None = cls.__menus.get(menu)

        if not m:
            raise MenuNotFoundError(menu)
        cls.__opened = m

    @classmethod
    def display(cls) -> None:
        """
        Displays the currently opened menu.

        If the opened menu is not a menu, raises a TypeError, otherwise
        displays the menu on the terminal.

        Args:
            none (None):

        Returns:
            none (None):

        Raises:
            TypeError
        """
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        cls.__opened.display()

    @classmethod
    def prompt(cls) -> str:
        """
        Prompts the user for an option.

        If the opened menu is not a menu, raises a TypeError, otherwise
        prompts the user.

        Args:
            none (None):

        Returns:
            none (None):

        Raises:
            TypeError
        """
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        return cls.__opened.prompt()

    @classmethod
    def display_error(cls, msg: str | None = None) -> None:
        """
        Display an error message on the terminal.

        Errors are always displays on top of menus in red. They are used to
        warn the user that their input was not valid. This is more of a
        notice than a real error that needs to be catched.

        Args:
            msg (str | None): Displays the error message. Default if none.

        Returns:
            none (None):
        """
        if not msg:
            msg = "INVALID OPTION. PLEASE CHOOSE A VALID OPTION"
        err: str = """╔═════════════════════════════════════════════════════╗
║ ERROR:                                              ║
╚═════════════════════════════════════════════════════╝"""

        err = bold(colorize(err, Color.DARK_RED))
        for c in err:
            print(c, end="", flush=True)
            sleep(0.0005)
        print("")
        move_up(2)
        move_right(9)
        print(f"m{bold(colorize(msg, Color.RED))}", end="")
        print("\n")

    @classmethod
    def set_opened_name(cls, name: str) -> None:
        """
        Sets the name of the opened menu.

        If the opened menu is not a menu, raises a TypeError, otherwise
        sets a new title to the menu.

        Args:
            name (str): The new title of the menu.

        Returns:
            none (None):

        Raises:
            TypeError
        """
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        cls.__opened.set_name(name)

    @classmethod
    def change_options(cls, options: List[str]) -> None:
        """
        Changes the options of a menu.

        If the opened menu is not a menu, raises a TypeError, otherwise
        changes the options of the menu to the provided ones. Mostly used
        to update the color of texts in menus.

        Args:
            options (List[str]): The new options.

        Returns:
            none (None):

        Raises:
            TypeError
        """
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        cls.__opened.change_options(options)

    @classmethod
    def change_value(cls, msg: str | None = None) -> int | None:
        """
        Display an input field on the terminal.

        Prompts the user with an input field, inviting them to enter a value.
        It is mostly used while changing the configuration of the maze.

        Args:
            msg (str | None): The input message. Default if none.

        Returns:
            val (int | None): The value entered by the user. None if invalid.
        """
        if not msg:
            msg = "NEW VALUE:"
        prmt: str = """╔═════════════════════════════════════════════════════╗
║                                                     ║
╚═════════════════════════════════════════════════════╝"""

        prmt = bold(colorize(prmt, Color.WHITE))
        for c in prmt:
            print(c, end="", flush=True)
            sleep(0.0005)
        print("")
        move_up(2)
        move_right(2)
        print(bold(colorize(msg, Color.WHITE)), end="")
        move_right(1)
        try:
            return int(input("m"))
        except (ValueError, TypeError):
            return None
