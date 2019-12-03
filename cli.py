import argparse
import os
from pathlib import Path
import sys

from __version import VERSION
import entrypoint

def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", 
        choices=sorted(["current", "version", "shell", "list", "info"]), 
        help="Possible actions")
    parser.add_argument(
        "env_name",
        default=None,
        nargs="?",
        help="Name of the environment to consider")
    return parser.parse_args(args)


def list_envs():
    root = entrypoint.ENVI_DIR
    print(f"Looking into `{root}`")
    if not root.exists():
        print("No defined environments")

    count = 0
    for file in root.glob("*.ini"):
        name = str(file.name).replace(".ini", "")
        print(f" - {name}")
        count += 1

    if count == 0:
        print("No defined environments")


def print_info():
        print("Envi")
        print(f"version: {VERSION}")
        print(f"Environment config directory: {entrypoint.ENVI_DIR}")


def main():
    args = parse_arguments(sys.argv[1:])
    if args.action == "version":
        print(f"Version {VERSION}")
    elif args.action == "current":
        env_name = os.getenv("ENVI_ENV_NAME", "(None)")
        print(f"Current env: {env_name}")
    elif args.action == "shell":
        forwarded_args = [arg for arg in sys.argv[1:] if arg != "shell"]
        entrypoint.generate(forwarded_args)
    elif args.action == "list":
        list_envs()
    elif args.action == "info":
        print_info()


if __name__ == "__main__":
    main()