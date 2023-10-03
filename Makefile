version = "0.1.0" # exo3d_tools/__init__.py


.PHONY: test
test:
	poetry run python -m pytest


.PHONY: publish
publish:
	poetry run python -m twine upload --repository astro ./dist/*