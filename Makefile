.PHONY: help docker-base-build docker-agent-build docker-agent-run minikube-start

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
	docker build -f Dockerfile.agent -t flock-agent .

docker-agent-run:
	docker run flock-agent
	

docker-embeddings-loader-build:
	docker build -f Dockerfile.embeddings_loader -t flock-embeddings-loader .	

docker-embeddings-loader-run:
	docker run flock-embeddings-loader


docker-webscraper-build:
	docker build -f Dockerfile.webscraper -t flock-webscraper .
	
docker-webscraper-run:
	docker run flock-webscraper


minikube-start:
	minikube start \
	--ports=127.0.0.1:27017:30200  \
	--ports=127.0.0.1:8200:30201  \
	--ports=127.0.0.1:5672:30202	\
	--ports=127.0.0.1:25672:30203  \
	--ports=127.0.0.1:15672:30204 \
	--cpus 4 --memory 6144
	@sleep 5
	minikube addons enable metrics-server 




load-images:
	minikube image load flock-agent
	minikube image load flock-embeddings-loader
	minikube image load flock-webscraper
	

# 27017:30200 # mongo
# 8200:30201 # vault
# 5672:30202 # rabbitMQ ampq
# 25672:30203 # rabbitMQ dist
# 15672:30204 # rabbitMQ manager


apply-mongo:
	kubectl apply -f infra/mongoDB/k8s

apply-rabbitmq:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update
	helm upgrade --install -f infra/rabbitMQ/values.yaml flock-queue bitnami/rabbitmq

delete-rabbitmq:
	helm delete flock-queue

apply-vault:
	helm repo add hashicorp https://helm.releases.hashicorp.com
	helm repo update
	helm upgrade --install -f infra/vault/values.yaml flock-secrets-store hashicorp/vault
	# kubectl exec -it flock-secrets-store-vault-0 -- vault operator init
	# kubectl exec -it flock-secrets-store-vault-0 -- vault operator unseal <key>

apply-infra: apply-mongo apply-rabbitmq apply-vault

apply-secret:
	kubectl apply -f infra/secret.yaml

apply-pvc:
	kubectl apply -f infra/pvc.yaml

setup-all: docker-base-build docker-agent-build docker-embeddings-loader-build docker-webscraper-build load-images apply-secret apply-pvc apply-infra
