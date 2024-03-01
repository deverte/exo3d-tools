ver := "0.2.0"

build:
  just update-version
  python3 -m build build

test:
  python3 -m pytest

publish:
  python3 -m twine upload --repository astro ./dist/*

update-version:
  #!/usr/bin/env python3
  import pathlib
  import re

  flake = pathlib.Path('flake.nix')
  pattern = 'version = ".*"; # managed'
  repl = 'version = "{{ver}}"; # managed'
  flake.write_text(re.sub(pattern, repl, flake.read_text()))

  pyproject = pathlib.Path('pyproject.toml')
  pattern = 'version = ".*"'
  repl = 'version = "{{ver}}"'
  pyproject.write_text(re.sub(pattern, repl, pyproject.read_text()))

  init = pathlib.Path('exo3d_tools/__init__.py')
  pattern = '__version__ = ".*"'
  repl = '__version__ = "{{ver}}"'
  init.write_text(re.sub(pattern, repl, init.read_text()))

  readme = pathlib.Path('README.md')
  pattern = '\/tags\/.*\.tar\.gz'
  repl = '/tags/{{ver}}.tar.gz'
  readme.write_text(re.sub(pattern, repl, readme.read_text()))