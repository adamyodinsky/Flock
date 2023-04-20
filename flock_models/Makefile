.PHONY: validate-resources validate-schemas write-openapi fomat lint

validate-resources:
	@echo "Validating resources"
	@poetry run python tests/resources_validation.py

validate-schemas:
	@echo "Validating schemas"
	@poetry run python tests/schemas_validation.py

format:
	@echo "Formatting code"
	@poetry run isort . && poetry run black . 

lint:
	@echo "Linting code"
	@poetry run pylint flock_scehmas tests --disable=E0401,F0001
	