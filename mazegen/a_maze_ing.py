from .utils import colorize, get_42logo_cells
from .input import InputHandler, InvalidOption
from .enums import MazeObject, Color, Limits
from .maze import Maze
from .config import Configuration
from sys import argv
from os import system


def change_config_display(config: Configuration) -> None:
    enx: int = config.entry_pos.x
    eny: int = config.entry_pos.y
    exx: int = config.exit_pos.x
    exy: int = config.exit_pos.y
    g: Color = Color.GREEN
    r: Color = Color.RED

    width: str = colorize(f"WIDTH: {config.width}", Color.WHITE)
    height: str = colorize(f"HEIGHT: {config.height}", Color.WHITE)
    entry: str = colorize(f"ENTRY: [{enx}, {eny}]", Color.WHITE)
    exit_label: str = colorize(f"EXIT: [{exx}, {exy}]", Color.WHITE)
    perfect: str = colorize("PERFECT", config.perfect and g or r)
    seed: str = colorize(f"SEED: {config.seed}", Color.WHITE)

    InputHandler.change_options([
        f"1 ║ {width}",
        f"2 ║ {height}",
        f"3 ║ {entry}",
        f"4 ║ {exit_label}",
        f"5 ║ {perfect}",
        f"6 ║ {seed}",
        f"0 ║ {colorize('GO BACK', Color.RED)}",
    ])


def change_anim_display(maze: bool, path: bool) -> None:
    on: Color = Color.GREEN
    off: Color = Color.RED
    maze_label: str = colorize("MAZE ANIMATION", maze and on or off)
    path_label: str = colorize("PATH ANIMATION", path and on or off)

    InputHandler.change_options([
        f"1 ║ {maze_label}",
        f"2 ║ {path_label}",
        f"0 ║ {colorize('GO BACK', Color.RED)}"
    ])


def loop(lab: Maze) -> None:
    prompt: str
    err: bool = False
    err_msg: str = ""
    obj: MazeObject
    val: int | None
    conf: Configuration
    x: int | None
    y: int | None

    while True:
        system("clear")
        if lab.get_status():
            lab.visualize()
            print("")
        if err:
            err = False
            InputHandler.display_error(err_msg)
            err_msg = ""
        InputHandler.display()
        try:
            prompt = InputHandler.prompt()
        except InvalidOption:
            err = True
            continue

        match prompt:
            case "GenerateMaze":
                lab.generate()
            case "SolveMaze":
                lab.generate(keep_seed=True, invert_solve=True)
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
                lab.switch_animation_state(MazeObject.WALL)
                state_wall = lab.get_animation_state(MazeObject.WALL)
                state_path = lab.get_animation_state(MazeObject.PATH)
                change_anim_display(state_wall, state_path)
            case "SwitchAnimPath":
                lab.switch_animation_state(MazeObject.PATH)
                state_wall = lab.get_animation_state(MazeObject.WALL)
                state_path = lab.get_animation_state(MazeObject.PATH)
                change_anim_display(state_wall, state_path)
            case "GoToOptions":
                InputHandler.goto("Options")
            case "GoToMazeOptions":
                InputHandler.goto("Maze")
                change_config_display(lab.get_config())
            case "ChangeWidth":
                val = InputHandler.change_value("WIDTH:")
                min_w: int = Limits.MIN_WIDTH.value
                max_w: int = Limits.MAX_WIDTH.value

                if not isinstance(val, int):
                    err = True
                    err_msg = "INVALID VALUE. PLEASE ENTER A NUMBER"
                else:
                    if val < min_w:
                        err = True
                        err_msg = f"WIDTH MUST BE GREATER OR EQUAL TO {min_w}"
                        continue
                    if val > max_w:
                        err = True
                        err_msg = f"WIDTH MUST BE LESSER OR EQUAL TO {max_w}"
                        continue
                    conf = lab.get_config()

                    conf.width = val
                    change_config_display(conf)
            case "ChangeHeight":
                val = InputHandler.change_value("HEIGHT:")
                min_h: int = Limits.MIN_HEIGHT.value
                max_h: int = Limits.MAX_HEIGHT.value

                if not isinstance(val, int):
                    err = True
                    err_msg = "INVALID VALUE. PLEASE ENTER A NUMBER"
                else:
                    if val < min_h:
                        err = True
                        err_msg = f"HEIGHT MUST BE GREATER OR EQUAL TO {min_h}"
                        continue
                    if val > max_h:
                        err = True
                        err_msg = f"HEIGHT MUST BE LESSER OR EQUAL TO {max_h}"
                        continue
                    conf = lab.get_config()

                    conf.height = val
                    change_config_display(conf)
            case "ChangeEntryPosition":
                conf = lab.get_config()

                x = InputHandler.change_value("X:")
                if not isinstance(x, int):
                    err = True
                    err_msg = "INVALID VALUE. PLEASE ENTER A NUMBER"
                else:
                    if x < 0 or x > conf.width - 1:
                        err = True
                        err_msg = "ENTRY CANNOT BE OFF BOUNDS"
                        continue
                    print("")
                    y = InputHandler.change_value("Y:")
                    if not isinstance(y, int):
                        err = True
                        err_msg = "INVALID VALUE. PLEASE ENTER A NUMBER"
                    else:
                        if y < 0 or y > conf.height - 1:
                            err = True
                            err_msg = "ENTRY CANNOT BE OFF BOUNDS"
                            continue
                        if (x, y) in get_42logo_cells(conf.width, conf.height):
                            err = True
                            err_msg = "ENTRY CANNOT BE ON 42 LOGO"
                            continue
                        conf.entry_pos.x = x
                        conf.entry_pos.y = y
                        change_config_display(conf)
            case "ChangeExitPosition":
                conf = lab.get_config()

                x = InputHandler.change_value("X:")
                if not isinstance(x, int):
                    err = True
                    err_msg = "INVALID VALUE. PLEASE ENTER A NUMBER"
                else:
                    if x < 0 or x > conf.width - 1:
                        err = True
                        err_msg = "EXIT CANNOT BE OFF BOUNDS"
                        continue
                    print("")
                    y = InputHandler.change_value("Y:")
                    if not isinstance(y, int):
                        err = True
                        err_msg = "INVALID VALUE. PLEASE ENTER A NUMBER"
                    else:
                        if y < 0 or y > conf.height - 1:
                            err = True
                            err_msg = "EXIT CANNOT BE OFF BOUNDS"
                            continue
                        if (x, y) in get_42logo_cells(conf.width, conf.height):
                            err = True
                            err_msg = "EXIT CANNOT BE ON 42 LOGO"
                            continue
                        conf.exit_pos.x = x
                        conf.exit_pos.y = y
                        change_config_display(conf)
            case "ChangePerfect":
                conf = lab.get_config()
                conf.perfect = not conf.perfect
                change_config_display(conf)
            case "ChangeSeed":
                val = InputHandler.change_value("SEED:")

                if not isinstance(val, int):
                    err = True
                else:
                    conf = lab.get_config()

                    conf.seed = val
                    change_config_display(conf)
            case "Exit":
                system("clear")
                exit(0)


def run() -> None:
    if len(argv) <= 1:
        print(f"Usage: python3 {argv[0]} <config file path>")
    else:
        system("clear")
        config_path = argv[1]
        try:
            config = Configuration.new(config_path)
        except Exception as e:
            print(f"Failed to load configuration file:\n{e}")
            exit(1)

        lab: Maze = Maze(config)
        loop(lab)
