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
	docker build -f Dockerfile.flock --target agent-stage -t flock-agent .
	minikube image load flock-agent

docker-embeddings-loader-build:
	docker build -f Dockerfile.flock --target embeddings-loader-stage -t flock-embeddings-loader .
	minikube image load flock-embeddings-loader

docker-agent-run:
	docker run flock-agent

docker-embeddings-loader-run:
	docker run flock-embeddings-loader


minikube-start:
	minikube start \
	--ports=127.0.0.1:443:443 \
	--ports=127.0.0.1:80:80 \
	--ports=127.0.0.1:27017:30200  \
	--ports=127.0.0.1:8200:30201  \
	--ports=127.0.0.1:5672:30202	\
	--ports=127.0.0.1:25672:30203  \
	--ports=127.0.0.1:15672:30204  


load-images:
	minikube image load flock-agent
	minikube image load flock-embeddings-loader
	minikube image load vault-init

# 27017:30200 # mongo
# 8200:30201 # vault
# 5672:30202 # rabbitMQ ampq
# 25672:30203 # rabbitMQ dist
# 15672:30204 # rabbitMQ manager


apply-mongo:
	kubectl apply -f utils/mongoDB/k8s

apply-rabbitmq:
	helm upgrade --install -f utils/rabbitMQ/values.yaml flock-queue bitnami/rabbitmq

delete-rabbitmq:
	helm delete flock-queue

apply-vault:
	docker build -f utils/vault/Dockerfile -t vault-init .
	helm install -f utils/vault/values.yaml flock-secret-store hashicorp/vault


# setup-vault:
# 	kubectl exec -it vault-0 -- vault operator init -key-shares=1 -key-threshold=1 -format=json > cluster-keys.json
# 	kubectl exec -it vault-0 -- vault operator unseal $(cat cluster-keys.json | jq -r ".unseal_keys_b64[]")
# 	kubectl exec -it vault-0 -- vault login $(cat cluster-keys.json | jq -r ".root_token")
# 	kubectl exec -it vault-0 -- vault secrets enable -path=secret kv-v2
# 	kubectl exec -it vault-0 -- vault kv put secret/flock-configs \
# 		flock-configs='{"mongo": {"host": "mongodb://mongo:27017"}, "rabbitmq": {"host": "amqp://guest:guest@flock-queue-rabbitmq:5672/"}}'