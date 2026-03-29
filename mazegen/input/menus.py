from typing import List
from abc import ABC, abstractmethod
from time import sleep


class InvalidOption(BaseException):
    """
    The InvalidOption class.

    A class derived from BaseException. Mostly raised when there was an
    invalid option picked from the available choices.
    """
    pass


class BaseMenu(ABC):
    """
    The BaseMenu class.

    An abstract class that acts as an interface for menu sub-classes.
    Most of the logic is also contained here.
    """
    def __init__(self, name: str, options: List[str]) -> None:
        """
        Initializes a new BaseMenu.

        Needs a title and options. It is then used for the entire UI and
        User Experience systems.

        Args:
            name (str): The title of the menu.
            options (list[str]): The options of the menu.
        """
        self.__options: List[str] = options
        self.__name: str = name

    def display(self) -> None:
        """
        Displays the menu on the terminal.

        Displays a window on the terminal. Shows up all the options of the menu
        as well as its title on the top left. The horizontal size is fixed but
        the vertical size changes according to the options.

        Args:
            none (None):

        Returns:
            none (None:
        """
        menu: str = ""
        top_bar: str = "╔═══╦═"
        bottom_bar: str = "╚═══╩═"
        bar_length: int = 32
        i: int = 1

        top_bar += f" {self.__name.upper()} "
        top_bar += ("═" * (bar_length - 2 - len(self.__name)))
        top_bar += "╗"
        bottom_bar += ("═" * bar_length)
        bottom_bar += "╝"
        for opt in self.__options:
            line: str = f"║ {opt}"
            line += (" " * (bar_length + 15 - len(line)))
            line += "║\n"
            menu += line
            i += 1
        for c in top_bar:
            print(c, end="", flush=True)
            sleep(0.0005)
        print("")
        for c in menu:
            print(c, end="", flush=True)
            sleep(0.0005)
        for c in bottom_bar:
            print(c, end="", flush=True)
            sleep(0.0005)
        print("")

    def set_name(self, name: str) -> None:
        """
        Sets the name of the menu.

        Used in some cases where the menu needs to be renamed for clarity
        purposes.

        Args:
            name (str): The new name.

        Returns:
            none (None):
        """
        self.__name = name

    @abstractmethod
    def prompt(self) -> str:
        """
        Prompts the user.

        This is an abstract method that needs to be implemented in all
        sub-classes.

        Args:
            none (None):

        Returns:
            option (str): The picked option by the user.
        """
        pass

    def change_options(self, options: List[str]) -> None:
        """
        Changes the options.

        This is mostly used for changing the color of the text.

        Args:
            options (list[str]): The new options.

        Returns:
            none (None):
        """
        self.__options = options


class MainMenu(BaseMenu):
    """
    The MainMenu sub-class.

    Inherits from the BaseMenu class. The only change is are the prompt method.
    Displays and manages the main window that users will see at the launch of
    the program.
    """
    def prompt(self) -> str:
        """
        Prompts the user with options.

        It has 5 available options.

        1) Generates a new maze.
        2) Solves the generated maze.
        3) Erases the maze.
        4) Goes to the options menu
        0) Quits the program.

        If the option is invalid, raises an error.

        Args:
            none (None):

        Returns:
            option (str): The option picked by the user.
        """
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
                return "GoToOptions"
            case 0:
                return "Exit"
            case _:
                raise InvalidOption


class ColorMenu(BaseMenu):
    """
    The ColorMenu sub-class.

    Inherits from the BaseMenu class. The only change is are the prompt method.
    Displays and manages the color menu, used to change the color of all parts
    of the maze.
    """
    def prompt(self) -> str:
        """
        Prompts the user with options.

        It has 9 available options.

        1) Sets the color to Gray.
        2) Sets the color to Red.
        3) Sets the color to Green.
        4) Sets the color to Yellow.
        5) Sets the color to Blue.
        6) Sets the color to Purple.
        7) Sets the color to Cyan.
        8) Sets the color to White.
        0) Goes back to the color options menu.

        If the option is invalid, raises an error.

        Args:
            none (None):

        Returns:
            option (str): The option picked by the user.
        """
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
            case 0:
                return "GoToColorOptions"
            case _:
                raise InvalidOption


class DisplayMenu(BaseMenu):
    """
    The DisplayMenu sub-class.

    Inherits from the BaseMenu class. The only change is are the prompt method.
    Displays and manages which part of the maze the user wishes to change the
    color of.
    """
    def prompt(self) -> str:
        """
        Prompts the user with options.

        It has 6 available options.

        1) Changes the color of the walls.
        2) Changes the color of the path.
        3) Changes the color of the entry.
        4) Changes the color of the exit.
        5) Changes the color of the 42 logo.
        0) Goes back to the options menu.

        If the option is invalid, raises an error.

        Args:
            none (None):

        Returns:
            option (str): The option picked by the user.
        """
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
            case 0:
                return "GoToOptions"
            case _:
                raise InvalidOption


class AnimMenu(BaseMenu):
    """
    The AnimMenu sub-class.

    Inherits from the BaseMenu class. The only change is are the prompt method.
    Displays and manages whether to animate the maze generation and/or the
    path animation.
    """
    def prompt(self) -> str:
        """
        Prompts the user with options.

        It has 3 available options.

        1) Toggles the animation of the maze.
        2) Toggles the animation of the path.
        0) Goes back to the options menu.

        If the option is invalid, raises an error.

        Args:
            none (None):

        Returns:
            option (str): The option picked by the user.
        """
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
            case 0:
                return "GoToOptions"
            case _:
                raise InvalidOption


class MazeMenu(BaseMenu):
    """
    The MazeMenu sub-class.

    Inherits from the BaseMenu class. The only change is are the prompt method.
    Displays and manages all the configuration of the maze. Useful if the user
    wishes to make changes to the maze.
    """
    def prompt(self) -> str:
        """
        Prompts the user with options.

        It has 7 available options.

        1) Sets the width of the maze.
        2) Sets the height of the maze.
        3) Sets the coordinates of the entry.
        4) Sets the coordinates of the exit.
        5) Toggles the perfect setting.
        6) Sets the seed of the maze.
        0) Goes back to the options menu.

        If the option is invalid, raises an error.

        Args:
            none (None):

        Returns:
            option (str): The option picked by the user.
        """
        res: int

        try:
            res = int(input("Choose an option: "))
        except (ValueError, TypeError):
            raise InvalidOption
        match res:
            case 1:
                return "ChangeWidth"
            case 2:
                return "ChangeHeight"
            case 3:
                return "ChangeEntryPosition"
            case 4:
                return "ChangeExitPosition"
            case 5:
                return "ChangePerfect"
            case 6:
                return "ChangeSeed"
            case 0:
                return "GoToOptions"
            case _:
                raise InvalidOption


class OptionsMenu(BaseMenu):
    """
    The OptionsMenu sub-class.

    Inherits from the BaseMenu class. The only change is are the prompt method.
    Displays and manages the pathways to the other options menus.
    """
    def prompt(self) -> str:
        """
        Prompts the user with options.

        It has 4 available options.

        1) Goes to the maze configuration.
        2) Goes to the color options.
        3) Goes to the animation options.
        0) Goes back to the main menu.

        If the option is invalid, raises an error.

        Args:
            none (None):

        Returns:
            option (str): The option picked by the user.
        """
        res: int

        try:
            res = int(input("Choose an option: "))
        except (ValueError, TypeError):
            raise InvalidOption
        match res:
            case 1:
                return "GoToMazeOptions"
            case 2:
                return "GoToColorOptions"
            case 3:
                return "GoToAnimationOptions"
            case 0:
                return "GoBackToMain"
            case _:
                raise InvalidOption
