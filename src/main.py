from sys import argv
from .config import Configuration
from .labyrinth import Cell
from .labyrinth import Labyrinth

if __name__ == "__main__":
    if len(argv) <= 1:
        print(f"Usage: python3 {argv[0]} <config file path>")
    else:
        config_path = argv[1]
        config = Configuration(config_path)

        lab = Labyrinth(config)
        lab.set_cell(0, 0, Cell(True, False, False, True))
        lab.set_cell(1, 0, Cell(False, False, False, True))
        lab.set_cell(1, 1, Cell(True, True, True, False))
        print(lab.convert_to_hex_str())
