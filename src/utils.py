def bool_from_string(string: str):
    match string.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            raise ValueError(f"Invalid boolean: {string}")
