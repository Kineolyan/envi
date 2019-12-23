import argparse
import configparser
import os
from pathlib import Path
import sys

import alias

def get_current_env(default = None):
    return os.getenv("ENVI_ENV_NAME", default)

def setup_env_info(env_name):
  print("## Environment information")
  print(f"export ENVI_ENV_NAME={env_name}")

def process_config(conf):
  d = conf["root-dir"]
  if d is not None:
    print(f"cd {d}")

def process_sdkman(tool, conf):
  version = conf["version"]
  print(f"sdk use {tool} {version}")

def process_asdf(tool, conf):
  version = conf["version"]
  print(f"asdf shell {tool} {version}")

def process_pipenv(tool, conf):
  pipenv_dir = conf.get("venv-dir", None)

  if pipenv_dir is not None: print(f"cd {pipenv_dir}")
  print("pipenv shell")
  if pipenv_dir is not None: print("cd -")

def process_bash(tool, conf):
  print(conf["command"])

def process_env(_ ,conf):
  for key in conf:
    if key != "module":
      value = conf[key]
      print(f"export {key}=\"{value}\"")

def process_alias(_, conf):
    contributed = False
    for key in conf:
        if key != "module":
            value = conf[key]
            alias.generate_alias_binary(key)
            env_key, env_value = alias.create_env_key(key, value)
            print(f"export {env_key}=\"{env_value}\"")
            contributed = True

    if contributed:
        alias_dir = str(alias.get_directory())
        current_path = os.getenv("PATH", "")
        print(f"export PATH={alias_dir}:{current_path}")

PROJECT_KEY = "--project--"
MODULES = {
  "alias": process_alias,
  "asdf": process_asdf,
  "bash": process_bash,
  "env": process_env,
  "pipenv": process_pipenv,
  "sdkman": process_sdkman
}
ENVI_DIR = Path.home() / ".config" / "envi"

def generate(args):
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("-f", "--file", help="Path to the file defining the env", default=None)
  arg_parser.add_argument("env_name", help="Name of the environment to setup")
  args = arg_parser.parse_args(args)

  env_name = args.env_name
  env_config_file = (ENVI_DIR / f"{env_name}.ini") if args.file is None else Path(args.file)

  config = configparser.ConfigParser()
  config.optionxform = str
  with env_config_file.open() as f: config.read_file(f)

  ## Set evalution command
  print("##! evaluate")
  setup_env_info(env_name)

  if PROJECT_KEY in config:
    print("## For the project configuration")
    process_config(config[PROJECT_KEY])
    print()

  for s in config:
    if s == "DEFAULT" or s == PROJECT_KEY:
      continue

    section = config[s]
    mod = section.get("module", None)
    print(f"## For `{s}`")
    MODULES[mod](s, section)
    print()

if __name__ == "__main__":
  generate(sys.argv[1:])
