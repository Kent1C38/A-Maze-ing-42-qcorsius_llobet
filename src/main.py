#!/usr/bin/python3.10

from sys import argv
from os import system
from .config import Configuration
from .maze import Maze
from .enums import MazeObject, Color
from .input import InputHandler, InvalidOption
from .utils import colorize


def loop(lab: Maze) -> None:
    prompt: str
    err: bool = False
    obj: MazeObject

    while True:
        system("clear")
        if lab.get_status():
            lab.visualize()
            print("")
        if err:
            err = False
            InputHandler.display_error()
        InputHandler.display()
        try:
            prompt = InputHandler.prompt()
        except InvalidOption:
            err = True
            continue

        match prompt:
            case "GenerateMaze":
                lab.generate()
            case "GoToColorOptions":
                InputHandler.goto("Display")
            case "ChangeWalls":
                InputHandler.goto("Color")
                InputHandler.set_opened_name("Color Menu | Walls")
                obj = MazeObject.WALL
            case "ChangePath":
                InputHandler.goto("Color")
                InputHandler.set_opened_name("Color Menu | Path")
                obj = MazeObject.PATH
            case "ChangeEntry":
                InputHandler.goto("Color")
                InputHandler.set_opened_name("Color Menu | Entry")
                obj = MazeObject.ENTRY
            case "ChangeExit":
                InputHandler.goto("Color")
                InputHandler.set_opened_name("Color Menu | Exit")
                obj = MazeObject.EXIT
            case "Change42":
                InputHandler.goto("Color")
                InputHandler.set_opened_name("Color Menu | 42")
                obj = MazeObject.FT
            case "SetGray":
                lab.set_color(obj, Color.DARK_GRAY)
                InputHandler.goto("Display")
            case "SetRed":
                lab.set_color(obj, Color.RED)
                InputHandler.goto("Display")
            case "SetGreen":
                lab.set_color(obj, Color.GREEN)
                InputHandler.goto("Display")
            case "SetYellow":
                lab.set_color(obj, Color.YELLOW)
                InputHandler.goto("Display")
            case "SetBlue":
                lab.set_color(obj, Color.BLUE)
                InputHandler.goto("Display")
            case "SetPurple":
                lab.set_color(obj, Color.PURPLE)
                InputHandler.goto("Display")
            case "SetCyan":
                lab.set_color(obj, Color.CYAN)
                InputHandler.goto("Display")
            case "SetWhite":
                lab.set_color(obj, Color.WHITE)
                InputHandler.goto("Display")
            case "GoBackToMain":
                InputHandler.goto("Main")
            case "GoBackToDisplay":
                InputHandler.goto("Display")
            case "GoToAnimationOptions":
                InputHandler.goto("Animation")
            case "HideMaze":
                lab.hide()
            case "SwitchAnimMaze":
                c_wall: Color
                state_wall: bool
                c_path: Color
                state_path: bool
                str_wall: str
                s_path: str

                lab.switch_animation_state(MazeObject.WALL)
                state_wall = lab.get_animation_state(MazeObject.WALL)
                state_path = lab.get_animation_state(MazeObject.PATH)
                c_wall = state_wall and Color.GREEN or Color.RED
                c_path = state_path and Color.GREEN or Color.RED
                str_wall = state_wall and "ON " or "OFF"
                s_path = state_path and "ON " or "OFF"
                InputHandler.change_options([
                    f"1 ║ MAZE ANIMATION: {colorize(str_wall, c_wall)}     ║\n"
                    f"║ 2 ║ PATH ANIMATION: {colorize(s_path, c_path)}     ║\n"
                    f"║ 3 ║ {colorize('GO BACK', Color.RED)}                 "
                ])
            case "SwitchAnimPath":
                c_wall: Color
                state_wall: bool
                c_path: Color
                state_path: bool
                str_wall: str
                s_path: str

                lab.switch_animation_state(MazeObject.PATH)
                state_wall = lab.get_animation_state(MazeObject.WALL)
                state_path = lab.get_animation_state(MazeObject.PATH)
                c_wall = state_wall and Color.GREEN or Color.RED
                c_path = state_path and Color.GREEN or Color.RED
                str_wall = state_wall and "ON " or "OFF"
                s_path = state_path and "ON " or "OFF"
                InputHandler.change_options([
                    f"1 ║ MAZE ANIMATION: {colorize(str_wall, c_wall)}     ║\n"
                    f"║ 2 ║ PATH ANIMATION: {colorize(s_path, c_path)}     ║\n"
                    f"║ 3 ║ {colorize('GO BACK', Color.RED)}                 "
                ])
            case "GoToOptions":
                InputHandler.goto("Options")
            case "GoToMazeOptions":
                InputHandler.goto("Maze")
            case "ChangeWidth":
                pass
            case "ChangeHeight":
                pass
            case "ChangeEntry":
                pass
            case "ChangeExit":
                pass
            case "ChangePerfect":
                pass
            case "ChangeSeed":
                pass
            case "Exit":
                system("clear")
                exit(0)


if __name__ == "__main__":
    if len(argv) <= 1:
        print(f"Usage: python3 {argv[0]} <config file path>")
    else:
        system("clear")
        config_path = argv[1]
        try:
            config = Configuration.new()
        except Exception as e:
            print(f"Failed to load configuration file:\n{e}")
            exit(1)

        lab: Maze = Maze(config)
        loop(lab)
