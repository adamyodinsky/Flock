.PHONY: help generate-server



generate-server:
	@openapi-generator generate -i openapi/Flock.json -g python-fastapi -o generator/server --package-name server --additional-properties=packageName=server

serve:
	@poetry run uvicorn flock_resources_server.main:app --reload --port 3000

test:
	@poetry run pytest tests -vv