from sys import argv
from .config import Configuration, ConfigValues

if __name__ == "__main__":
    if len(argv) <= 1:
        print(f"Usage: python3 {argv[0]} <config file path>")
    else:
        config_path = argv[1]
        config = Configuration(config_path)

        print(config.get(ConfigValues.EXIT))
