#!/usr/bin/python3.10

# --- IMPORTS -----------------------------------------------------------------

from typing import Dict, List
from .menus import BaseMenu, MainMenu, ColorMenu, DisplayMenu, AnimMenu
from ..utils import colorize, bold
from ..enums import Color

# --- EXCEPTIONS --------------------------------------------------------------


class MenuNotFoundError(BaseException):
    def __init__(self, menu: str):
        super().__init__(f"Cannot go to menu \"{menu}\"")

# --- CLASSES -----------------------------------------------------------------


class InputHandler:
    __menus: Dict[str, BaseMenu] = {
        "Main": MainMenu("Main Menu", [
            f"1 ║ {colorize('GENERATE MAZE', Color.WHITE)}",
            f"2 ║ {colorize('SOLVE MAZE', Color.WHITE)}",
            f"3 ║ {colorize('UNLOAD MAZE', Color.YELLOW)}",
            f"4 ║ {colorize('COLOR OPTIONS', Color.WHITE)}",
            f"5 ║ {colorize('ANIMATION OPTIONS', Color.WHITE)}",
            f"6 ║ {colorize('EXIT', Color.RED)}",
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
            f"9 ║ {colorize('GO BACK', Color.RED)}",
        ]),
        "Animation": AnimMenu("Animation Menu", [
            f"1 ║ MAZE ANIMATION: {colorize('OFF', Color.RED)}",
            f"2 ║ PATH ANIMATION: {colorize('OFF', Color.RED)}",
            f"3 ║ {colorize('GO BACK', Color.RED)}",
        ]),
        "Display": DisplayMenu("Display Menu", [
            f"1 ║ {colorize('WALLS', Color.WHITE)}",
            f"2 ║ {colorize('PATH', Color.WHITE)}",
            f"3 ║ {colorize('ENTRY', Color.WHITE)}",
            f"4 ║ {colorize('EXIT', Color.WHITE)}",
            f"5 ║ {colorize('42 LOGO', Color.WHITE)}",
            f"6 ║ {colorize('GO BACK', Color.RED)}",
        ]),
    }
    __opened: BaseMenu = __menus.get("Main")

    @classmethod
    def goto(cls, menu: str) -> None:
        m: BaseMenu | None = cls.__menus.get(menu)

        if not m:
            raise MenuNotFoundError(menu)
        cls.__opened = m

    @classmethod
    def display(cls) -> None:
        cls.__opened.display()

    @classmethod
    def prompt(cls) -> None:
        return cls.__opened.prompt()

    @classmethod
    def display_error(cls) -> None:
        err: str = """╔═════════════════════════════════════════════════════╗
║ ERROR: INVALID OPTION. PLEASE CHOOSE A VALID OPTION ║
╚═════════════════════════════════════════════════════╝"""

        print(bold(colorize(err, Color.DARK_RED)))

    @classmethod
    def set_opened_name(cls, name: str) -> None:
        cls.__opened.set_name(name)

    @classmethod
    def change_options(cls, options: List[str]) -> None:
        cls.__opened.change_options(options)
