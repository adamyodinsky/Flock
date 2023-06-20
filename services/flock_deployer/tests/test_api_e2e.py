import os

import requests
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory

from flock_deployer.config_store import ConfigStoreFactory
from flock_deployer.deployer import DeployerFactory
from flock_deployer.schemas.config import DeploymentConfigSchema
from flock_deployer.schemas.request import (
    ConfigRequest,
    DeleteRequest,
    DeploymentRequest,
)
from flock_deployer.schemas.response import (
    ConfigCreated,
    HealthResponse,
    ResourceCreated,
    ResourceDeleted,
)

os.environ["LOCAL"] = "true"
DRY_RUN = os.environ.get("DRY_RUN", True)
HOST = os.environ.get("FLOCK_DEPLOYER_HOST", "localhost")
PORT = os.environ.get("FLOCK_DEPLOYER_PORT", "9000")
resource_store = ResourceStoreFactory.get_resource_store()
secret_store = SecretStoreFactory.get_secret_store("vault")
config_store = ConfigStoreFactory.get_store("mongo")


def setup_deployers():
    return DeployerFactory.get_deployer(
        deployer_type=os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"),
        secret_store=secret_store,
        resource_store=resource_store,
        config_store=config_store,
    )


deployers = setup_deployers()


def test_health():
    response = requests.get(f"http://{HOST}:{PORT}/health")

    HealthResponse.validate(response.json())

    assert response.status_code == 200


def test_put_config():
    example_config = deployers.config_store.load_file(
        "./assets/schemas/configs/example_config.yaml"
    )
    response = requests.put(
        "http://localhost:9000/config",
        json={"config": example_config},
    )

    assert response.status_code == 200
    ConfigCreated.validate(response.json())


def test_get_config():
    response = requests.get(
        "http://localhost:9000/config/example",
    )

    assert response.status_code == 200
    DeploymentConfigSchema.validate(response.json())


def test_delete_config():
    response = requests.delete(
        "http://localhost:9000/config/example",
    )

    assert response.status_code == 200
    ResourceDeleted.validate(response.json())


def put_deployment(deployment_kind, resource_name, resource_kind):
    example_config = deployers.config_store.load_file(
        "./assets/schemas/configs/example_config.yaml"
    )
    response = requests.put(
        f"http://{HOST}:{PORT}/deployment",
        json={
            "deployment_name": "example",
            "deployment_namespace": "default",
            "deployment_kind": deployment_kind,
            "resource_name": resource_name,
            "resource_namespace": "default",
            "resource_kind": resource_kind,
            "config": example_config,
            "dry_run": DRY_RUN,
        },
    )

    assert response.status_code == 200
    ResourceCreated.validate(response.json())


def put_deployment_cronjob(deployment_kind, resource_name, resource_kind):
    example_config = deployers.config_store.load_file(
        "./assets/schemas/configs/example_config.yaml"
    )
    response = requests.put(
        f"http://{HOST}:{PORT}/deployment",
        json={
            "deployment_name": "example",
            "deployment_namespace": "default",
            "deployment_kind": deployment_kind,
            "resource_name": resource_name,
            "resource_namespace": "default",
            "resource_kind": resource_kind,
            "config": example_config,
            "dry_run": DRY_RUN,
        },
    )

    assert response.status_code == 200
    ResourceCreated.validate(response.json())


def delete_deployment(deployment_kind):
    response = requests.delete(
        f"http://{HOST}:{PORT}/deployment",
        json={
            "deployment_name": "example",
            "deployment_namespace": "default",
            "deployment_kind": deployment_kind,
        },
    )

    assert response.status_code == 200
    ResourceDeleted.validate(response.json())


def test_deployment():
    put_deployment(
        deployment_kind="FlockDeployment",
        resource_name="my-agent",
        resource_kind="Agent",
    )
    if not DRY_RUN:
        delete_deployment(
            deployment_kind="FlockDeployment",
        )


def test_job():
    put_deployment(
        deployment_kind="FlockJob",
        resource_name="my-web-scraper",
        resource_kind="WebScraper",
    )
    if not DRY_RUN:
        delete_deployment(
            deployment_kind="FlockJob",
        )


def test_cronjob():
    put_deployment(
        deployment_kind="FlockCronJob",
        resource_name="meta",
        resource_kind="EmbeddingsLoader",
    )
    if not DRY_RUN:
        delete_deployment(
            deployment_kind="FlockCronJob",
        )
