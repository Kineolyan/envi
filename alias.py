from pathlib import Path
import re
import shutil
import tempfile

ALIAS_DIR = Path("/tmp") / "envi" / "aliases"

def get_directory():
  return ALIAS_DIR

def check_binary(binary):
  if re.search("\s", binary):
    raise ValueError(f"Binary in alias must not contain spaces. Got: `{binary}`")

def env_binary_var(binary):
  upper_binary = re.sub(r"[\-]+", "_", binary.upper())
  return f"ENVI_ALIAS_{upper_binary}"

def write_alias_binary(out, binary):
  out.write(b"#!/bin/bash\n")
  var = env_binary_var(binary)
  out.write(b"exec $")
  out.write(var.encode("utf8"))
  out.write(b" $*\n")

def generate_alias_binary(binary):
  ALIAS_DIR.mkdir(parents=True, exist_ok=True)
  binary_path = ALIAS_DIR / binary
  if not binary_path.exists():
    with tempfile.NamedTemporaryFile() as out:
      write_alias_binary(out, binary)
      out.seek(0)

      shutil.copyfile(out.name, str(binary_path))
      binary_path.chmod(0o755)

def create_env_key(binary, target):
  env_var = env_binary_var(binary)
  return (env_var, target)