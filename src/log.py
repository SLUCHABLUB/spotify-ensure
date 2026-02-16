from sys import stderr


# TODO: Use colours.
def _log(level: str, message: str) -> None:
    print(f"[{level}]: {message}", file=stderr)


def error(message: str) -> None:
    _log("ERROR", message)


def warn(message: str) -> None:
    _log("WARNING", message)
