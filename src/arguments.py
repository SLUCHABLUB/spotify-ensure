from sys import argv, stderr


def print_usage() -> None:
    executable = argv[0]

    print(f"USAGE: {executable} <ensure.toml>", file=stderr)


def get_ensure_file_path() -> str:
    if len(argv) != 2:
        print_usage()
        exit(1)

    return argv[1]
