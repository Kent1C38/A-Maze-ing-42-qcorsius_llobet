from .position import Position
from .utils import bool_from_string, is_pos_valid, get_42logo_cells
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from random import randint
import sys


class InvalidConfiguration(Exception):
    def __init__(self, args):
        super().__init__(args)


class Configuration(BaseModel):
    width: int = Field(strict=True, ge=11, le=100)
    height: int = Field(strict=True, ge=9, le=100)
    entry_pos: Position = Field(strict=True)
    exit_pos: Position = Field(strict=True)
    output_file: str = Field(strict=True)
    perfect: bool = Field(strict=True)
    seed: Optional[int] = Field(strict=True)

    @model_validator(mode='after')
    def validator(self) -> "Configuration":
        if not is_pos_valid(self.entry_pos.x, self.entry_pos.y,
                            bounds=(self.width, self.height)):
            raise InvalidConfiguration("Entry is not in the maze bounds")

        if not is_pos_valid(self.exit_pos.x, self.exit_pos.y,
                            bounds=(self.width, self.height)):
            raise InvalidConfiguration("Exit is not in the maze bounds")

        if not self.output_file.endswith((".txt", ".maze", ".mf")):
            raise InvalidConfiguration("Output file must endby one of the "
                                       "following extension: .txt, .maze, .mf")

        if (self.entry_pos.x, self.entry_pos.y) in \
                get_42logo_cells(self.width, self.height):
            raise InvalidConfiguration("Entry cannot be one of the 42 logo's "
                                       "cells")

        if (self.exit_pos.x, self.exit_pos.y) in \
                get_42logo_cells(self.width, self.height):
            raise InvalidConfiguration("Exit cannot be one of the 42 logo's "
                                       "cells")
        return self

    def replace_seed(self, new_seed: int):
        self.seed = new_seed

    @staticmethod
    def new() -> "Configuration":
        temp = dict()
        try:
            with open("config.txt", "r") as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    key = key.lower()

                    match key:
                        case "width" | "height" | "seed":
                            try:
                                temp[key] = int(value)
                            except Exception:
                                temp[key] = None
                        case "output_file":
                            temp[key] = value
                        case "perfect":
                            temp[key] = bool_from_string(value)
                        case "entry" | "exit":
                            try:
                                temp[key] = Position.from_str(value)
                            except Exception:
                                temp[key] = None
        except Exception as e:
            raise Exception(f"Error occured during config file reading: {e}")

        return Configuration(
            width=temp.get("width", None),
            height=temp.get("height", None),
            seed=temp.get("seed", randint(-sys.maxsize - 1, sys.maxsize)),
            output_file=temp.get("output_file", None),
            perfect=temp.get("perfect", None),
            entry_pos=temp.get("entry", None),
            exit_pos=temp.get("exit", None)
        )
