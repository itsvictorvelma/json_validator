import json
import argparse
from pathlib import Path
import sys

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


def is_valid_json():
    try:
        with open(args.filepath, "r", encoding="utf-8") as json_file:
            json.load(json_file)
            print("is valid json")
            sys.exit(0)

    except ValueError:
        print("not valid json")
        sys.exit(1)

    except FileNotFoundError:
        print("Cannot find targeted file - please ensure the filepath is correct")
        sys.exit(1)

    except PermissionError:
        print("PERMISSION DENIED: you are not cool enough to open up this file.")
        sys.exit(1)


is_valid_json()
