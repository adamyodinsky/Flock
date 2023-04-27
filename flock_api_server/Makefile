.PHONY: help generate-server

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  generate-server    to generate server from openapi spec"

generate-server:
	@openapi-generator generate -i external_api_tools/apimatic/Flock.json -g python-fastapi -o api_server --package-name api_server --additional-properties=packageName=api_server
