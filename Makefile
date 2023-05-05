.PHONY: help build build-base build-agent

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build         Build all images"
	@echo "  build-base  	 Build base image"
	@echo "  build-agent   Build agent image"

docker-base-build:
	docker build -f Dockerfile.python.base -t flock-python-base   .

# docker-agent-builde:
# 	docker build -f Dockerfile.flock.base --target -t flock-agent . 


# setup dev environment