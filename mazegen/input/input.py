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
    def __init__(self, menu: str) -> None:
        super().__init__(f"Cannot go to menu \"{menu}\"")

# --- CLASSES -----------------------------------------------------------------


class InputHandler:
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
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        m: BaseMenu | None = cls.__menus.get(menu)

        if not m:
            raise MenuNotFoundError(menu)
        cls.__opened = m

    @classmethod
    def display(cls) -> None:
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        cls.__opened.display()

    @classmethod
    def prompt(cls) -> str:
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        return cls.__opened.prompt()

    @classmethod
    def display_error(cls, msg: str | None = None) -> None:
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
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        cls.__opened.set_name(name)

    @classmethod
    def change_options(cls, options: List[str]) -> None:
        if not isinstance(cls.__opened, BaseMenu):
            raise TypeError("Opened menu must be a valid Menu object")
        cls.__opened.change_options(options)

    @classmethod
    def change_value(cls, msg: str | None = None) -> int | None:
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
