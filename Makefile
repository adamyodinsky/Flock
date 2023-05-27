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

docker-agent-build:
	docker build -f Dockerfile.flock --target agent-stage -t flock-agent .
	minikube image load flock-agent

docker-embeddings-loader-build:
	docker build -f Dockerfile.flock --target embeddings-loader-stage -t flock-embeddings-loader .
	minikube image load flock-embeddings-loader

docker-agent-run:
	docker run flock-agent

docker-embeddings-loader-run:
	docker run flock-embeddings-loader