.PHONY: run-dev format lint install build test-publish test

install:
	poetry install

run-dev:
	@echo "Running in development mode"
	@poetry run uvicorn flock_agent.main:app --reload  

format:
	@echo "Formatting code"
	@poetry run isort . && poetry run black . 

lint:
	@echo "Linting code"
	@poetry run pylint flock_scehmas tests --disable=E0401,F0001

install:
	@echo "Installing dependencies"
	@poetry install

test:
	@echo "Running tests"
	@poetry run pytest

build: test install
	@echo "Building Docker image"
	@pip freeze > requirements.txt
	# @docker build -t flock-agent .
