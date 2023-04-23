.PHONY: validate-resources validate-schemas write-openapi fomat lint

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  validate-resources  to validate the resources"
	@echo "  validate-schemas    to validate the schemas"
	@echo "  write-openapi       to write the openapi"
	@echo "  format              to format the code"
	@echo "  lint                to lint the code"
	@echo "  build               to build the package"

validate-resources:
	@echo "Validating resources"
	@poetry run python tests/resources_validation.py

format:
	@echo "Formatting code"
	@poetry run isort . && poetry run black . 

lint:
	@echo "Linting code"
	@poetry run pylint flock_scehmas tests --disable=E0401,F0001
	
build:
	@echo "Building package"
	@poetry build
	