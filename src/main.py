from sys import argv
from .config import Configuration
from .labyrinth import Labyrinth

if __name__ == "__main__":
    if len(argv) <= 1:
        print(f"Usage: python3 {argv[0]} <config file path>")
    else:
        config_path = argv[1]
        config = Configuration(config_path)

        lab = Labyrinth(config, debug=True)
        print(lab.convert_to_hex_str())

        lab.generate()

        print(lab.convert_to_hex_str())
