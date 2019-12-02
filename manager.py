from __version import VERSION

import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", 
        choices=["current", "version"], 
        help="Possible actions")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.action == "version":
        print(f"Version {VERSION}")
    if args.action == "current":
        env_name = os.getenv("ENVI_ENV_NAME", "(None)")
        print(f"Current env: {env_name}")


if __name__ == "__main__":
    main()