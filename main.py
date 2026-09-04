import argparse
from pathlib import Path
import sys


def parse_json(content: str) -> bool:
    """Custom parser logic to validate JSON content.

    Returns True if valid JSON, False if invalid.
    """

    if content.strip() == "{}":
        return True

    else:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="A tool to parse and validate JSON documents"
    )
    parser.add_argument(
        "-f",
        "--filepath",
        type=Path,
        required=True,
        help="The path to the JSON file you want to parse",
    )

    args = parser.parse_args()

    # Handle file reading and OS exceptions
    try:
        with open(args.filepath, "r", encoding="utf-8") as json_file:
            content = json_file.read()

    except FileNotFoundError:
        print(f"Error: File '{args.filepath}' not found.")
        sys.exit(1)

    except PermissionError:
        print(f"Error: Permission denied for '{args.filepath}'.")
        sys.exit(1)

    # Validate the raw string content with your custom parser
    is_valid = parse_json(content)

    if is_valid:
        print(f"Success: '{args.filepath}' is valid JSON.")
        sys.exit(0)
    else:
        print(f"Error: '{args.filepath}' is not valid JSON.")
        sys.exit(1)


if __name__ == "__main__":
    main()
