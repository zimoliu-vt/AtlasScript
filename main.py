
import sys
from pathlib import Path

from atlasscript.parser import parse
from atlasscript.interpreter import Interpreter


def run_file(filename):
    path = Path(filename)

    if not path.is_file():
        print(f"Error: File not found: {filename}")
        return 1

    if path.suffix != ".atlas":
        print("Error: Expected a .atlas file")
        return 1

    try:
        source = path.read_text(encoding="utf-8")

        program = parse(source)

        interpreter = Interpreter()
        interpreter.run(program)

        return 0

    except (
        SyntaxError,
        NameError,
        ZeroDivisionError,
        TypeError,
        RuntimeError,
    ) as error:
        print(f"AtlasScript error: {error}")
        return 1


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.atlas>")
        return 1

    return run_file(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
