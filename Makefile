.PHONY: help build build-poetry build-agent

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build         Build all images"
	@echo "  build-poetry  Build poetry image"
	@echo "  build-agent   Build agent image"

build-poetry:
	@docker build -t flock-poetry -f Dockerfile.poetry .

build-agent:
	@docker build -t flock-agent -f Dockerfile.agent .
