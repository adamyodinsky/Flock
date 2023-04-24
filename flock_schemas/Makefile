.PHONY: validate-schemas write-openapi

validate-schemas:
	@echo "Validating Schemas\n"
	@poetry run python tests/schemas_validation.py

write-openapi:
	@echo "Writing OpenAPI Schemas\n"
	@poetry run python scripts/openapi_sync.py

format:
	@echo "Formatting Code\n"
	@poetry run isort . && poetry run black . 

lint:
	@echo "Linting Code\n"`
	@poetry run pylint flock_scehmas tests

build:
	@echo "Building Package\n"
	@poetry build

create-stubs:
	@poetry run stubgen -p flock_schemas -o .
	