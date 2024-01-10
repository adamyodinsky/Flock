.PHONY: help format lint build test test_api_e2e test-deployer write-json-schemas load-global-config

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  format            to format the code"
	@echo "  lint              to lint the code"
	@echo "  build             to build the package"
	@echo "  test              to run the tests"
	@echo "  test_api_e2e      to run the e2e tests"
	@echo "  test-deployer     to run the deployer tests"
	@echo "  write-json-schemas to write the json schemas"
	@echo "  load-global-config to load the global config"


format:
	poetry run isort . && poetry run black . 

lint:
	poetry run pylint flock_scehmas tests

build:
	
	poetry build

write-json-schemas:
	poetry run python scripts/write_json_schemas.py

load-configs:
	poetry run python scripts/load_configs.py

test:
	poetry run pytest tests

test-deployer:
	poetry run pytest tests/test_deployer.py

test_api_e2e:
	poetry run pytest tests/test_api_e2e.py
