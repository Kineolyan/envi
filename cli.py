import argparse
import os
import sys

from __version import VERSION
import entrypoint

def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", 
        choices=["current", "version", "shell"], 
        help="Possible actions")
    parser.add_argument(
        "env_name",
        action="store_const",
        const=None)
    return parser.parse_args(args)


def main():
    args = parse_arguments(sys.argv[1:])
    if args.action == "version":
        print(f"Version {VERSION}")
    if args.action == "current":
        env_name = os.getenv("ENVI_ENV_NAME", "(None)")
        print(f"Current env: {env_name}")
    if args.action == "shell":
        forwarded_args = [arg for arg in sys.argv[1:] if arg != "shell"]
        entrypoint.generate(forwarded_args)


if __name__ == "__main__":
    main()