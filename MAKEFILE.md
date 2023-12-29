# Makefile Documentation

The `Makefile` consists of several commands to facilitate building, running, and maintaining dockerized applications and kubernetes resources.

## Docker Commands

- `docker-base-build`: Builds the base Python docker image.
- `docker-deployer-build`: Builds the deployer docker image.
- `docker-observer-build`: Builds the observer docker image.
- `docker-resources-server-build`: Builds resources server docker image.
- `docker-agent-build`: Builds the agent docker image.
- `docker-embeddings-loader-build`: Builds the embeddings loader docker image.
- `docker-webscraper-build`: Builds the webscraper docker image.
- `docker-proxy-build`: Builds the proxy docker image located in the infra/flock_proxy folder.
- `docker-build-all`: Builds all docker images.
- `docker-deployer-run`: Runs the deployer docker image.
- `docker-observer-run`: Runs the observer docker image.
- `docker-resources-server-run`: Runs resources server docker image.
- `docker-agent-run`: Runs the agent docker image.
- `docker-embeddings-loader-run`: Runs the embeddings loader docker image.
- `docker-webscraper-run`: Runs the webscraper docker image with environment variables.
- `docker-proxy-run`: Runs the proxy docker image.

## Kubernetes and Minikube Commands

- `minikube-start`: Starts a local instance of Minikube with specific port mappings.
- `load-webscraper`, `load-agent`, `load-embeddings-loader`, `load-deployer`, `load-observer`, `load-resources-server`, `load-proxy`: These commands unload the respective docker images and load them into Minikube.
- `load-images`: Executes all image loader commands for Minikube.
- `apply-mongo`, `delete-mongo`: Apply or delete MongoDB kubernetes resources respectively.
- `apply-deployer`, `delete-deployer`: Apply or delete deployer kubernetes resources respectively.
- `apply-observer`, `delete-observer`: Apply or delete observer kubernetes resources respectively.
- `apply-resources-server`, `delete-resources-server`: Apply or delete resources server kubernetes resources respectively.
- `apply-rabbitmq`, `delete-rabbitmq`: Apply or delete RabbitMQ using Helm.
- `apply-vault`, `delete-vault`: Apply or delete Vault using Helm.
- `apply-ingress`: Apply ingress resources.
- `apply-proxy`, `delete-proxy`: Apply or delete proxy kubernetes resources respectively.
- `reload-proxy`, `reload-resources-server`, `reload-observer`, `reload-deployer`: Delete, rebuild, reload and apply the respective kubernetes resources.
- `apply-secret`: Apply secret resources.
- `apply-pvc`: Apply PVC resources.
- `apply-all`: Apply secret, PVC, MongoDB, Vault, RabbitMQ, deployer, observer, resources server, ingress and proxy kubernetes resources.
- `delete-apps`: Delete deployer, observer and resources server kubernetes resources.

## Schema and Resources Commands

- `validate-resources`: Validates resources using `make validate-resources` in `libs/flock_resources`.
- `write-schemas`: Writes json schemas to `libs/flock_schemas` using `make write-json-schemas`.
- `schemas-setup`: Validates and writes json schemas to `libs/flock_schemas`, and uploads json schemas to db.
- `fill-db-with-data`: Executes `schemas-setup` and `validate-resources`.

## Miscellaneous Commands

- `setup-docker`: Builds all docker images and loads them into Minikube.
- `start-services`: Applies all kubernetes resources, validates resources, writes schemas, and fills db with data.
- `setup-start-all`: Executes `setup-docker` and `start-services`.
- `reload-all`: Reloads deployer, observer, resources server and proxy.
- `ngrok`: Starts Ngrok on port 80 and rewrites the host header.

Please use `make <target>` where `<target>` represents the appropriate command. Note that some commands may depend on others to run

# Starting Local Development Environment

To set up and start your local development environment, follow the steps outlined below.

## 1. Build Docker Images

First, you need to build all the relevant docker images. Run the following command:

```bash
make docker-build-all
```

This command builds all the necessary docker images including base Python image, deployer, observer, resources server, agent, embeddings loader, webscraper, and proxy.

## 2. Load Images into Minikube

Next, load the Docker images into Minikube. Run the following command:

```bash
make load-images
```

This command takes each built docker image and loads them into your local Minikube cluster.

## 3. Start Minikube

Then, you need to start Minikube. Run the following command:

```bash
make minikube-start
```

This command starts a local Minikube cluster with the specified port mappings.

## 4. Apply Kubernetes Resources

After starting Minikube, you can apply all the Kubernetes resources. Run the following command:

```bash
make apply-all
```

This command applies secret, PVC, MongoDB, Vault, RabbitMQ, deployer, observer, resources server, ingress, and proxy Kubernetes resources.

## 5. Write and Validate Schemas

Next, ensure that your JSON schemas are written and validated by running:

```bash
make write-schemas
make validate-resources
```

The `write-schemas` command generates JSON schemas in the `libs/flock_schemas` directory, and `validate-resources` command validates resources using the schemas.

## 6. Fill the Database with Data

Before starting your services, fill the database with data:

```bash
make fill-db-with-data
```

This command fills the database with necessary data.

## 7. Start Services

Finally, you can start all the services. Run the following command:

```bash
make start-services
```

This command applies all the Kubernetes resources, validates the resources, writes the schemas, and fills the database with data. Now, all services are ready, and you can proceed with your development tasks.
