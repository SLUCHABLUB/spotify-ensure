@check:
    uvx pyrefly check
    uvx ruff check

@run *arguments: check
    uv run src/main.py {{ arguments }}
