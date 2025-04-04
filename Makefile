.PHONY: build
build:
	sphinx-build -b html docs/source/ docs/build/html
	python -m build
	twine check dist/*

.PHONY: clean
clean:
	rm -rf docs/build/html
	rm -rf dist
	rm -rf src/thurible.egg-info
	rm -rf examples/__pycache__
	rm -rf tests/__pycache__
	rm -rf src/thurible/__pycache__

.PHONY: docs
docs:
	sphinx-build -b html docs/source/ docs/build/html

.PHONY: pre
pre:
	poetry run tox
	poetry run python precommit.py
	git status

.PHONY: test
test:
	poetry run pytest --capture=sys

.PHONY: testv
testv:
	poetry run pytest -vv --capture=sys