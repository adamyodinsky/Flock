.PHONY: help build build-base build-agent

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build         Build all images"
	@echo "  build-base  	 Build base image"
	@echo "  build-agent   Build agent image"

build-base:
	@docker build -t flock-base -f Dockerfile.base .

build-agent:
	@docker build -t flock-agent -f Dockerfile.agent .
