.PHONY: build

PIP = pip
PYTHON = python

build:
	${PYTHON} -m build

install:
	${PIP} install . -U

install-editable:
	${PIP} install -e . --config-settings editable_mode=compat -U

test:
	ruff check --target-version=py38 .