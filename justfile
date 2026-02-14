@check:
    uvx pyrefly check
    uvx ruff check

@run: check
    uv run src/main.py
