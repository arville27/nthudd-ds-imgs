import json
from pathlib import Path
from types import FunctionType
from typing import Dict


def read_file(filename: Path | str) -> str:
    with open(filename, "r") as f:
        return f.read().strip()


def write_file(filename: Path | str, content: str) -> bool:
    try:
        with open(filename, "w") as f:
            f.write(content.strip())
        return True
    except Exception as e:
        print(e)
        return False


def read_json(filename: Path | str) -> Dict | list:
    return json.loads(read_file(filename))


def log_stdout(content: str, log_function: FunctionType) -> None:
    print(content)
    log_function(content)
