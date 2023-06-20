.PHONY: help format lint build create-stubs

format:
	poetry run isort . && poetry run black . 

lint:
	poetry run pylint flock_scehmas tests

build:
	
	poetry build

write-json-schemas:
	poetry run python scripts/write_json_schemas.py

test:
	poetry run pytest tests