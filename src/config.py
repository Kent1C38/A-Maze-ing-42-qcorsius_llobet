from .position import Position
from .utils import bool_from_string, is_pos_valid
from enum import Enum
from typing import Any


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
    SEED = "seed"


class Configuration:
    def __init__(self, config_file_path: str):
        self.__config = {}

        try:
            with open(config_file_path, "r") as config_file:

                current_line = 1
                needed_val = [conf_val.value for conf_val in ConfigValues]

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
                            case "width" | "height" | "seed":
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

            if (self.get(ConfigValues.HEIGHT) *
                    self.get(ConfigValues.WIDTH)) > 47*48:
                raise InvalidConfiguration("Invalid size: cannot excede 48x47"
                                           + " or 47x48")

            if (self.get(ConfigValues.WIDTH) <= 0
                    or self.get(ConfigValues.HEIGHT) <= 0):
                raise InvalidConfiguration("Invalid dimenstions: width and" +
                                           " height cannot be 0 or negative")

            self.__validity_check()

        except Exception as e:
            print(
                f"{type(e).__name__} caught while "
                f"preparing maze configuration: {e}")
            exit(1)

    def replace_seed(self, new_seed: int) -> None:
        self.__config[ConfigValues.SEED.value] = new_seed

    def get(self, parameter: ConfigValues) -> Any:
        return self.__config[parameter.value]

    def __validity_check(self):
        entry: Position = self.get(ConfigValues.ENTRY)
        ext: Position = self.get(ConfigValues.EXIT)

        bounds = (self.get(ConfigValues.WIDTH), self.get(ConfigValues.HEIGHT))

        if (entry.get_x() == ext.get_x()) and (entry.get_y() == ext.get_y()):
            raise InvalidConfiguration("Entry and exit cannot be at the same"
                                       "position!")

        if not is_pos_valid(entry.get_x(), entry.get_y(), bounds):
            raise InvalidConfiguration("Invalid Entry: Out of bounds!")

        if not is_pos_valid(ext.get_x(), ext.get_y(), bounds):
            raise InvalidConfiguration("Invalid Exit: Out of bounds!")
