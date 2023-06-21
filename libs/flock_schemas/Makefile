.PHONY: help install validate-schemas write-json-schemas upload-json-schemas-to-db write-upload-schemas format lint build

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install             to install the dependencies"

	@echo "  validate-schemas    to validate the schemas"
	@echo "  write-openapi       to write the openapi"
	@echo "  format              to format the code"
	@echo "  lint                to lint the code"
	@echo "  build               to build the package"

install:
	@poetry install


format:
	@echo "Formatting code"
	@poetry run isort . && poetry run black . 

lint:
	@echo "Linting code"
	@poetry run pylint flock_scehmas tests --disable=E0401,F0001
	
build:
	@echo "Building package"
	@poetry build
	

validate-schemas:
	@echo "Validating Schemas\n"
	@poetry run python tests/schemas_validation.py

write-json-schemas:
	@poetry run python scripts/write_json_schemas.py

upload-json-schemas-to-db:
	@poetry run python scripts/upload_json_schemas_to_db.py

write-upload-schemas: write-json-schemas upload-json-schemas-to-db


