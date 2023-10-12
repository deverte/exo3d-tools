version = "0.1.2" # exo3d_tools/__init__.py, pyproject.toml


.PHONY: build
build:
	poetry build


.PHONY: test
test:
	poetry run python -m pytest


.PHONY: publish
publish:
	poetry run python -m twine upload --repository astro ./dist/*