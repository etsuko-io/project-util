.PHONY: install

install:
	pip install -e .

style:
	isort . && black .
	pre-commit run --all-files
