.PHONY: help format lint build create-stubs

format:
	@echo "Formatting Code\n"
	@poetry run isort . && poetry run black . 

lint:
	@echo "Linting Code\n"`
	@poetry run pylint flock_scehmas tests

build:
	@echo "Building Package\n"
	@poetry build

write-json-schemas:
	@poetry run python scripts/write_json_schemas.py