.PHONY: install

install:
	pip install -e .

style:
	isort . && black .
	pre-commit run --all-files

install-local:
	pip install -r requirements-local.txt

test:
	pytest src/tests -vv
