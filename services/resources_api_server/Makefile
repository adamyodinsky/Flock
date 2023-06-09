.PHONY: help generate-server

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  generate-server    to generate server from openapi spec"

generate-server:
	@openapi-generator generate -i openapi/Flock.json -g python-fastapi -o generator/server --package-name server --additional-properties=packageName=server

serve:
	@poetry run uvicorn server.main:app --reload --port 3000