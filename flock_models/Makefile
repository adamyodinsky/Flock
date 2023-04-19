.PHONY: validate-resources validate-schemas write-openapi fomat lint

validate-resources:
	poetry run python tests/resources_validation.py

validate-schemas:
	poetry run python tests/schemas_validation.py

write-openapi:
	poetry run python scripts/openapi_sync.py

format:
	poetry run isort . && poetry run black . 

lint:
	poetry run pylint flock_scehmas tests --disable=E0401,F0001