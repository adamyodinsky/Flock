.PHONY: run-dev format lint install build test-publish test

install:
	poetry install

run-dev:
	@poetry run python flock_embeddings_loader/main.py

	
format:
	@poetry run isort . && poetry run black . 

lint:
	@poetry run pylint flock_scehmas tests --disable=E0401,F0001

install:
	@echo "Installing dependencies"
	@poetry install

test:
	@poetry run pytest
