from typing import List
from abc import ABC, abstractmethod


class InvalidOption(BaseException):
    pass


class BaseMenu(ABC):
    def __init__(self, name: str, options: List[str]) -> None:
        self.__options: List[str] = options
        self.__name: str = name

    def display(self) -> None:
        menu: str = ""
        top_bar: str = "╔═══╦═══"
        bottom_bar: str = "╚═══╩═══"
        i: int = 1

        top_bar += f" {self.__name.upper()} "
        for _ in range(20 - len(self.__name)):
            top_bar += "═"
        top_bar += "╗"
        bottom_bar += f" {self.__name.upper()} "
        for _ in range(20 - len(self.__name)):
            bottom_bar += "═"
        bottom_bar += "╝"
        for opt in self.__options:
            line: str = f"║ {opt}"

            for _ in range(39 - len(line)):
                line += " "
            line += "║\n"
            menu += line
            i += 1
        print(top_bar)
        print(menu, end="")
        print(bottom_bar)

    def set_name(self, name: str) -> None:
        self.__name = name

    @abstractmethod
    def prompt(self) -> None:
        pass

    def change_options(self, options: List[str]) -> None:
        self.__options = options


class MainMenu(BaseMenu):
    def prompt(self) -> str:
        res: int

        try:
            res = int(input("Choose an option: "))
        except (ValueError, TypeError):
            raise InvalidOption
        match res:
            case 1:
                return "GenerateMaze"
            case 2:
                return "SolveMaze"
            case 3:
                return "HideMaze"
            case 4:
                return "GoToColorOptions"
            case 5:
                return "GoToAnimationOptions"
            case 6:
                return "Exit"
            case _:
                raise InvalidOption


class ColorMenu(BaseMenu):
    def prompt(self) -> str:
        res: int

        try:
            res = int(input("Choose an option: "))
        except (ValueError, TypeError):
            raise InvalidOption
        match res:
            case 1:
                return "SetGray"
            case 2:
                return "SetRed"
            case 3:
                return "SetGreen"
            case 4:
                return "SetYellow"
            case 5:
                return "SetBlue"
            case 6:
                return "SetPurple"
            case 7:
                return "SetCyan"
            case 8:
                return "SetWhite"
            case 9:
                return "GoBackToDisplay"
            case _:
                raise InvalidOption


class DisplayMenu(BaseMenu):
    def prompt(self) -> str:
        res: int

        try:
            res = int(input("Choose an option: "))
        except (ValueError, TypeError):
            raise InvalidOption
        match res:
            case 1:
                return "ChangeWalls"
            case 2:
                return "ChangePath"
            case 3:
                return "ChangeEntry"
            case 4:
                return "ChangeExit"
            case 5:
                return "Change42"
            case 6:
                return "GoBackToMain"
            case _:
                raise InvalidOption


class AnimMenu(BaseMenu):
    def prompt(self) -> str:
        res: int

        try:
            res = int(input("Choose an option: "))
        except (ValueError, TypeError):
            raise InvalidOption
        match res:
            case 1:
                return "SwitchAnimMaze"
            case 2:
                return "SwitchAnimPath"
            case 3:
                return "GoBackToMain"
            case _:
                raise InvalidOption
