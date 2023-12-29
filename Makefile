.PHONY: help docker-base-build docker-agent-build docker-agent-run docker-embeddings-loader-build docker-embeddings-loader-run docker-webscraper-build docker-webscraper-run docker-deployer-build docker-deployer-run docker-build-all

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  docker-base-build to build the base python image"
	@echo "  docker-agent-build to build the agent image"
	@echo "  docker-agent-run to run the agent image"
	@echo "  docker-embeddings-loader-build to build the embeddings loader image"
	@echo "  docker-embeddings-loader-run to run the embeddings loader image"
	@echo "  docker-webscraper-build to build the webscraper image"
	@echo "  docker-webscraper-run to run the webscraper image"
	@echo "  docker-deployer-build to build the deployer image"
	@echo "  docker-deployer-run to run the deployer image"
	@echo "  docker-build-all to build all the images"
	@echo "  minikube-start to start minikube"
	@echo "  load-images to load the images into minikube"
	@echo "  apply-mongo to apply the mongoDB k8s resources"
	@echo "  apply-deployer to apply the deployer k8s resources"
	@echo "  apply-rabbitmq to apply the rabbitMQ k8s resources"
	@echo "  apply-vault to apply the vault k8s resources"
	@echo "  apply-secret to apply the secret k8s resources"
	@echo "  apply-pvc to apply the pvc k8s resources"
	@echo "  setup-all to build all the images and apply all the k8s resources"
	@echo "  apply-infra to apply all the k8s resources"
	

docker-base-build:
	docker build -f Dockerfile.python.base -t flock-python-base   .

docker-deployer-build:
	docker build -f Dockerfile.deployer -t flock-deployer .

docker-observer-build:
	docker build -f Dockerfile.observer -t flock-observer .

docker-resources-server-build:
	docker build -f Dockerfile.resources_server -t flock-resources-server .

docker-agent-build:
	docker build -f Dockerfile.agent -t flock-agent .

docker-embeddings-loader-build:
	docker build -f Dockerfile.embeddings_loader -t flock-embeddings-loader .	

docker-webscraper-build:
	docker build -f Dockerfile.webscraper -t flock-webscraper .


docker-proxy-build:
	cd infra/flock_proxy; docker build -f Dockerfile.proxy -t flock-proxy .

docker-build-all: docker-base-build docker-agent-build docker-embeddings-loader-build docker-webscraper-build docker-deployer-build docker-observer-build docker-resources-server-build docker-proxy-build

docker-deployer-run:
	docker run --rm flock-deployer

docker-observer-run:
	docker run --rm flock-observer

docker-resources-server-run:
	docker run --rm flock-resources-server

docker-agent-run:
	docker run --rm -e LOCAL=true flock-deployer


docker-embeddings-loader-run:
	docker run --rm flock-embeddings-loader
	
docker-webscraper-run:
	docker run --rm \
	-e SCRAPER_NAME="test_spider" \
	-e SCRAPER_START_URLS="http://books.toscrape.com/catalogue/category/books/romance_8/index.html" \
	-e RULE_SCRAPER_ALLOWED_DOMAINS="books.toscrape.com" \
	-e RULE_SCRAPER_ALLOW="/catalogue/category/books/romance_8 /catalogue/category/books/philosophy_7" \
	-e RULE_SCRAPER_DENY_EXTENSIONS="" \
	-e SCRAPER_OUTPUT_DIR="/app/spider_output" \
	-e SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT=10 \
	--name flock_webscraper_test \
	-v ${PWD}/.spider_output:/app/spider_output \
	flock-webscraper

docker-proxy-run:
	docker run --rm flock-proxy

.PHONY: minikube-start

minikube-start:
	minikube start \
	--ports=0.0.0.0:80:32080 \
	--ports=127.0.0.1:443:32443 \
	--ports=127.0.0.1:27017:30200  \
	--ports=127.0.0.1:8200:30201  \
	--ports=127.0.0.1:5672:30202	\
	--ports=127.0.0.1:25672:30203  \
	--ports=127.0.0.1:15672:30204 \
	--ports=127.0.0.1:9000:30205 \
	--ports=127.0.0.1:9001:30206 \
	--ports=127.0.0.1:9002:30207 \
	# --cpus 4 --memory 6144
	@sleep 5
	minikube addons enable metrics-server

# 80:32080 # ingress http
# 443:32443 # ingress https
# 27017:30200 # mongo
# 8200:30201 # vault
# 5672:30202 # rabbitMQ ampq
# 25672:30203 # rabbitMQ dist
# 15672:30204 # rabbitMQ manager
# 9000:30205 # flock-deployer
# 9001:30206 # flock-observer
# 9002:30207 # flock-resources-server

.PHONY: load-webscraper load-agent load-embeddings-loader load-deployer load-observer load-resources-server load-proxy load-images

load-webscraper:
	minikube image unload flock-webscraper
	minikube image load flock-webscraper

load-agent:
	minikube image unload flock-agent
	minikube image load flock-agent

load-embeddings-loader:
	minikube image unload flock-embeddings-loader
	minikube image load flock-embeddings-loader

load-deployer:
	minikube image unload flock-deployer
	minikube image load flock-deployer

load-observer:
	minikube image unload flock-observer
	minikube image load flock-observer

load-resources-server:
	minikube image unload flock-resources-server
	minikube image load flock-resources-server

load-proxy:
	minikube image unload flock-proxy
	minikube image load flock-proxy

load-images: load-webscraper load-agent load-embeddings-loader load-deployer load-observer load-resources-server load-proxy

.PHONY: apply-mongo delete-mongo apply-deployer delete-deployer apply-observer delete-observer apply-resources-server delete-resources-server apply-rabbitmq delete-rabbitmq apply-vault delete-vault apply-ingress apply-proxy delete-proxy reload-proxy apply-secret apply-pvc validate-resources write-schemas validate-flock-schemas upload-schemas fill-db-with-data apply-all delete-apps setup-all

apply-mongo:
	kubectl apply -f infra/mongoDB/k8s

delete-mongo:
	kubectl delete -f infra/mongoDB/k8s

apply-deployer:
	kubectl apply -f infra/deployer

delete-deployer:
	kubectl delete -f infra/deployer

apply-observer:
	kubectl apply -f infra/observer

delete-observer:
	kubectl delete -f infra/observer

apply-resources-server:
	kubectl apply -f infra/resources_server

delete-resources-server:
	kubectl delete -f infra/resources_server

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
	
apply-vault-operator:
	helm upgrade --install vault-secrets-operator -f infra/vault_operator/values.yaml -n vault-secrets-operator-system --create-namespace hashicorp/vault-secrets-operator

delete-vault-operator:
	helm delete vault-secrets-operator -n vault-secrets-operator-system

apply-ingress:
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
	helm repo update
	helm upgrade --install -f infra/ingress/helm/values.yaml nginx-ingress ingress-nginx/ingress-nginx
	sleep 60 # waitng for ingress to be ready
	kubectl apply -f infra/ingress/k8s

apply-proxy:
	kubectl apply -f infra/flock_proxy/k8s

delete-proxy:
	kubectl delete -f infra/flock_proxy/k8s

reload-proxy: delete-proxy docker-proxy-build load-proxy apply-proxy
reload-resources-server: delete-resources-server docker-resources-server-build load-resources-server apply-resources-server
reload-observer: delete-observer docker-observer-build load-observer apply-observer
reload-deployer: delete-deployer docker-deployer-build load-deployer apply-deployer

apply-secret:
	kubectl apply -f infra/secret.yaml

apply-pvc:
	kubectl apply -f infra/pvc.yaml

validate-resources:
	cd libs/flock_resources; make validate-resources

write-schemas:
	cd libs/flock_schemas; make write-json-schemas

schemas-setup:
	cd libs/flock_schemas; make validate-schemas
	cd libs/flock_schemas; make write-json-schemas
	cd libs/flock_schemas; make upload-json-schemas-to-db

fill-db-with-data: schemas-setup validate-resources

apply-all: apply-secret apply-pvc apply-mongo apply-vault apply-rabbitmq apply-deployer apply-observer apply-resources-server apply-ingress apply-proxy

delete-apps: delete-deployer delete-observer delete-resources-server



setup-docker: docker-build-all load-images

start-services: apply-all validate-resources write-schemas fill-db-with-data

setup-start-all: setup-docker start-services

reload-all: reload-deployer reload-observer reload-resources-server reload-proxy

ngrok:
	ngrok http 80 --host-header=rewrite # --basic-auth="$(NGROK_USERNAME):$(NGROK_PASSWORD)"
