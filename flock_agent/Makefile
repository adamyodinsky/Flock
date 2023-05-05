.PHONY: run-dev format lint install build test-publish test

install:
	poetry install

run-dev:
	@echo "Running in development mode"
	@poetry run uvicorn flock_agent.main:app --reload  

run-prod:
	@echo "Running in production mode"
	@poetry run uvicorn flock_agent.main:app --host
	
format:
	@poetry run isort . && poetry run black . 

lint:
	@poetry run pylint flock_scehmas tests --disable=E0401,F0001

install:
	@echo "Installing dependencies"
	@poetry install

test:
	@poetry run pytest

test_curl:
	@curl -X POST -H "Content-Type: application/json" -d '{ "msg": "who is the president of USA?" }' localhost:8000/agent

docker-build: test install
	@echo "Building Docker image"
	@version=$$(poetry version | awk '{print $$2}') && \
	docker build -t flock-agent:${version} .
