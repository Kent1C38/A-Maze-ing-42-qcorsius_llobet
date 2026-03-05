from .position import Position
from .utils import bool_from_string, is_pos_in_boundaries
from enum import Enum


class InvalidConfiguration(Exception):
    def __init__(self, args):
        super().__init__(args)


class ConfigValues(Enum):
    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit"
    OUTPUT_FILE = "output_file"
    PERFECT = "perfect"


class Configuration:
    def __init__(self, config_file_path: str):
        self.__config = {}

        try:
            with open(config_file_path, "r") as config_file:

                current_line = 1
                needed_val = ["width", "height", "entry", "exit",
                              "output_file", "perfect"]

                for line in config_file.readlines():
                    clean_line = line.replace('\n', '')
                    splited = clean_line.split('=')
                    if len(splited) != 2:
                        raise InvalidConfiguration(
                            "Invalid parameter syntax at line " +
                            f"{current_line} (KEY=VALUE)")
                    else:
                        key = splited[0]
                        val = splited[1]

                        match key.lower():
                            case "width" | "height":
                                self.__config[key.lower()] = int(val)
                                needed_val.remove(key.lower())

                            case "entry" | "exit":
                                pos = Position.from_str(val)
                                self.__config[key.lower()] = pos
                                needed_val.remove(key.lower())

                            case "perfect":
                                self.__config[key.lower()] = bool_from_string(
                                    val)
                                needed_val.remove(key.lower())

                            case "output_file":
                                self.__config[key.lower()] = val
                                needed_val.remove(key.lower())

                            case _:
                                raise InvalidConfiguration(
                                    f"Unknown config parameter: '{key}' " +
                                    f"(line {current_line})")

                    current_line += 1

                if not len(needed_val) == 0:
                    raise InvalidConfiguration(
                        f"Missing parameters in config file: {needed_val}"
                    )

        except Exception as e:
            print(f"Error preparing maze configuration: {e}")
            exit(1)

    def get(self, parameter: ConfigValues) -> dict:
        return self.__config[parameter.value]
