#!/usr/bin/python3.10

from sys import argv, stdout
from os import system
from .config import Configuration
from .maze import Maze
from .enums import MazeObject, Color
from .utils import colorize, bold
from .ui import WindowManager, Window
from .position import Position as Vec2
from pynput.keyboard import Key, Listener

if __name__ == "__main__":
    manager: WindowManager = WindowManager()

    def on_press(key: str | Key) -> None:
        act: Window = manager.get_active()

        if key == Key.down:
            idx: int = act.move_down()
            print(idx)
            line: str = act.read(idx)

            act.write(colorize(line, Color.BLUE), Vec2(x=2, y=idx), idx)
        if key == Key.up:
            idx: int = act.move_up()
            line: str = act.read(idx)

            act.write(colorize(line, Color.BLUE), Vec2(x=2, y=idx), idx)

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
        manager.display_title()
        manager.main.set_color(Color.RED)
        manager.display_main_menu()
        

        with Listener(on_press=on_press) as listen:
            listen.join()
