""" Test """

import os
import time

import yaml
from flock_common import init_logging
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from flock_schemas.factory import SchemaFactory

from flock_deployer.config_store import ConfigStoreFactory
from flock_deployer.deployer import DeployerFactory
from flock_deployer.schemas.config import DeploymentConfigSchema
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.job import CronJobSchema, JobSchema


def set_dry_run():
    dry_run = os.environ.get("DRY_RUN", "true")

    if dry_run.lower() == "true":
        return True
    else:
        return False


DRY_RUN = set_dry_run()
SLEEP_TIME = 6

os.environ["LOCAL"] = "true"
init_logging(level="INFO")


resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.environ.get("RESOURCE_STORE_TYPE", "mongo"),
    db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
    host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
    port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
    username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
    password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
)

secret_store = SecretStoreFactory.get_secret_store(
    store_type=os.environ.get("SECRET_STORE_TYPE", "vault"),
    host=os.environ.get("SECRET_STORE_HOST", "http://localhost:8200"),
    token=os.environ.get("SECRET_STORE_TOKEN", "root"),
)

config_store = ConfigStoreFactory.get_store(
    store_type=os.environ.get("CONFIG_STORE_TYPE", "mongo"),
    db_name=os.environ.get("CONFIG_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("CONFIG_STORE_TABLE_NAME", "flock_configs"),
    host=os.environ.get("CONFIG_STORE_HOST", "localhost"),
    port=int(os.environ.get("CONFIG_STORE_PORT", 27017)),
    username=os.environ.get("CONFIG_STORE_USERNAME", "root"),
    password=os.environ.get("CONFIG_STORE_PASSWORD", "password"),
)


def setup_deployers():
    return DeployerFactory.get_deployer(
        deployer_type=os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"),
        secret_store=secret_store,
        resource_store=resource_store,
        config_store=config_store,
    )


schema_factory = SchemaFactory()
deployers = setup_deployers()


def load_and_validate_schema(schema_class, yaml_path):
    with open(yaml_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return schema_class.validate(data)


def process_manifest(deployer, deployment_manifest, target_manifest):
    deployer.deploy(deployment_manifest, target_manifest, dry_run=DRY_RUN)


def deploy(deployer, deployment_manifest):
    resource_manifest = resource_store.get(
        name=deployment_manifest.spec.targetResource.name,
        kind=deployment_manifest.spec.targetResource.kind,
        namespace=deployment_manifest.spec.targetResource.namespace,
    )
    target_schema_cls = schema_factory.get_schema(resource_manifest["kind"])
    target_manifest = target_schema_cls.validate(resource_manifest)

    process_manifest(deployer, deployment_manifest, target_manifest)


def create_manifest(
    target_name, target_namespace, target_kind, deployment_kind, config
) -> tuple:
    """
    Test manifest creator

    Args:
        target_name (str): Target name
        target_namespace (str): Target namespace
        target_kind (str): Target kind
        deployment_kind (str): Deployment kind
        config (DeploymentConfigSchema): Deployment config

    Returns:
        tuple: (target_manifest, deployment_manifest)
    """
    target_manifest = resource_store.get(
        name=target_name, kind=target_kind, namespace=target_namespace
    )
    creator_func = deployers.get_creator(deployment_kind)

    extra_args = {}
    if deployment_kind == "FlockCronJob":
        extra_args["schedule"] = "0 0 * * 0"

    deployment_manifest = creator_func(
        name=target_name,
        namespace=target_namespace,
        target_manifest=schema_factory.get_schema(target_kind).validate(
            target_manifest
        ),
        config=config,
        **extra_args,
    )
    return target_manifest, deployment_manifest


def delete(target_name, target_namespace, deployer):
    deployer.delete(
        name=target_name,
        namespace=target_namespace,
        dry_run=DRY_RUN,
    )


def test_integration():
    # Deploy Global Config
    global_config = deployers.config_store.load_file(
        "./assets/schemas/configs/global_config.yaml"
    )
    agent_config = deployers.config_store.load_file(
        "./assets/schemas/configs/agent_config.yaml"
    )
    webscraper_config = deployers.config_store.load_file(
        "./assets/schemas/configs/webscraper_config.yaml"
    )
    embeddingsloader_config = deployers.config_store.load_file(
        "./assets/schemas/configs/embeddingsloader_config.yaml"
    )
    example_config = deployers.config_store.load_file(
        "./assets/schemas/configs/example_config.yaml"
    )

    global_config = DeploymentConfigSchema.validate(global_config)
    deployers.config_store.put(global_config.dict())

    agent_config = DeploymentConfigSchema.validate(agent_config)
    deployers.config_store.put(agent_config.dict())

    webscraper_config = DeploymentConfigSchema.validate(webscraper_config)
    deployers.config_store.put(webscraper_config.dict())

    embeddingsloader_config = DeploymentConfigSchema.validate(embeddingsloader_config)
    deployers.config_store.put(embeddingsloader_config.dict())

    example_config = DeploymentConfigSchema.validate(example_config)
    deployers.config_store.put(example_config.dict())

    # Deploy WebScraper
    print("Deploying WebScraper Job")
    deployment_manifest = load_and_validate_schema(
        JobSchema, "./assets/schemas/webscraper_job.yaml"
    )
    deploy(deployers.job_deployer, deployment_manifest)

    # if not DRY_RUN:
    #     time.sleep(SLEEP_TIME)
    #     print("Deleting WebScraper Job")
    #     deployers.job_deployer.delete(
    #         name=deployment_manifest.metadata.name,
    #         namespace=deployment_manifest.namespace,
    #         dry_run=DRY_RUN,
    #     )

    # Deploy WebSCraper CronJob
    print("Deploying WebScraper CronJob")
    deployment_manifest = load_and_validate_schema(
        CronJobSchema, "./assets/schemas/webscraper_cronjob.yaml"
    )
    deploy(deployers.cronjob_deployer, deployment_manifest)

    # if not DRY_RUN:
    #     time.sleep(SLEEP_TIME)
    #     print("Deleting WebScraper CronJob")
    #     deployers.cronjob_deployer.delete(
    #         name=deployment_manifest.metadata.name,
    #         namespace=deployment_manifest.namespace,
    #         dry_run=DRY_RUN,
    #     )

    # Deploy EmbeddingsLoader
    print("Deploying EmbeddingsLoader Job")
    deployment_manifest = load_and_validate_schema(
        JobSchema, "./assets/schemas/embeddingsloader_job.yaml"
    )
    deploy(deployers.job_deployer, deployment_manifest)

    # if not DRY_RUN:
    #     time.sleep(SLEEP_TIME)
    #     print("Deleting EmbeddingsLoader Job")
    #     deployers.job_deployer.delete(
    #         name=deployment_manifest.metadata.name,
    #         namespace=deployment_manifest.namespace,
    #         dry_run=DRY_RUN,
    #     )

    # Deploy Agent
    print("Deploying Agent Deployment and Service")
    deployment_manifest = load_and_validate_schema(
        DeploymentSchema,
        "./assets/schemas/agent_deployment.yaml",
    )
    deploy(
        deployers.deployment_deployer,
        deployment_manifest,
    )

    deploy(deployers.service_deployer, deployment_manifest)

    if not DRY_RUN:
        time.sleep(SLEEP_TIME)
        print("Deleting Agent Deployment and Service")
        deployers.deployment_deployer.delete(
            name=deployment_manifest.metadata.name, namespace="default", dry_run=DRY_RUN
        )
        deployers.service_deployer.delete(
            name=deployment_manifest.metadata.name, namespace="default", dry_run=DRY_RUN
        )

    # Deploy WebScraper with manifest creators
    print("\n######## Manifest Creators to Deployers Test ##########\n")

    print("Deploying WebScraper Job")
    _, deployment_manifest = create_manifest(
        "my-web-scraper", "default", "WebScraper", "FlockJob", example_config
    )
    deploy(deployers.job_deployer, deployment_manifest)

    if not DRY_RUN:
        time.sleep(SLEEP_TIME)
        print("Deleting WebScraper Job")
        deployers.job_deployer.delete(
            name=deployment_manifest.metadata.name,
            namespace=deployment_manifest.namespace,
            dry_run=DRY_RUN,
        )

    print("Deploying WebScraper CronJob")
    _, deployment_manifest = create_manifest(
        "my-web-scraper", "default", "WebScraper", "FlockCronJob", example_config
    )
    deploy(deployers.cronjob_deployer, deployment_manifest)

    if not DRY_RUN:
        time.sleep(SLEEP_TIME)
        print("Deleting WebScraper CronJob")
        deployers.cronjob_deployer.delete(
            name=deployment_manifest.metadata.name,
            namespace=deployment_manifest.namespace,
            dry_run=DRY_RUN,
        )

    print("Deploying EmbeddingsLoader Job")
    _, deployment_manifest = create_manifest(
        "embeddings-loader", "default", "EmbeddingsLoader", "FlockJob", example_config
    )
    deploy(deployers.job_deployer, deployment_manifest)

    if not DRY_RUN:
        time.sleep(SLEEP_TIME)
        print("Deleting EmbeddingsLoader Job")
        deployers.job_deployer.delete(
            name=deployment_manifest.metadata.name,
            namespace=deployment_manifest.namespace,
            dry_run=DRY_RUN,
        )

    print("Deploying Agent Deployment and Service")
    _, deployment_manifest = create_manifest(
        "my-agent", "default", "Agent", "FlockDeployment", example_config
    )
    deploy(deployers.deployment_deployer, deployment_manifest)
    deploy(deployers.service_deployer, deployment_manifest)

    if not DRY_RUN:
        time.sleep(SLEEP_TIME)
        print("Deleting Agent Deployment and Service")
        deployers.deployment_deployer.delete(
            name=deployment_manifest.metadata.name,
            namespace=deployment_manifest.namespace,
            dry_run=DRY_RUN,
        )
        deployers.service_deployer.delete(
            name=deployment_manifest.metadata.name,
            namespace=deployment_manifest.namespace,
            dry_run=DRY_RUN,
        )

    deployers.config_store.delete("example")


if __name__ == "__main__":
    test_integration()
