.PHONY: validate-resources validate-schemas write-openapi

validate-resources:
	poetry run python tests/resources_validation.py

validate-schemas:
	poetry run python tests/schemas_validation.py

write-openapi:
	poetry run python scripts/openapi_sync.py
