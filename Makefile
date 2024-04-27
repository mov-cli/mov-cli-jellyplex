.PHONY: build

pip = pip3.8
python = python

build:
	${python} -m build

install:
	${pip} install . -U

install-editable:
	${pip} install -e . --config-settings editable_mode=compat -U

test:
	ruff check --target-version=py38 .