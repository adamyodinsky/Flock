""" Test """

import os

import yaml
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from flock_schemas.factory import SchemaFactory

from flock_deployer.config_store import ConfigStoreFactory
from flock_deployer.deployer import DeployerFactory
from flock_deployer.schemas.config import DeploymentConfigSchema
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.job import JobSchema

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


schema_factory = SchemaFactory()
deployers = setup_deployers()
DRY_RUN = False


def load_and_validate_schema(schema_class, yaml_path):
    with open(yaml_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return schema_class.validate(data)


def process_manifest(deployer, deployment_manifest, target_manifest, dry_run):
    deployer.deploy(deployment_manifest, target_manifest, dry_run=dry_run)


def test_deployer(deployer, deployment_manifest, dry_run=DRY_RUN):
    resource_manifest = resource_store.get(
        name=deployment_manifest.spec.targetResource.name,
        kind=deployment_manifest.spec.targetResource.kind,
        namespace=deployment_manifest.spec.targetResource.namespace,
    )
    target_schema_cls = schema_factory.get_schema(resource_manifest["kind"])
    target_manifest = target_schema_cls.validate(resource_manifest)

    process_manifest(deployer, deployment_manifest, target_manifest, dry_run)


def test_manifest_creator(
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
    deployment_manifest = creator_func(
        name=target_name,
        namespace=target_namespace,
        target_manifest=schema_factory.get_schema(target_kind).validate(
            target_manifest
        ),
        config=config,
    )
    return target_manifest, deployment_manifest


def delete(target_name, target_namespace, deployer, dry_run=DRY_RUN):
    deployer.delete(
        name=target_name,
        namespace=target_namespace,
        dry_run=dry_run,
    )


def main():
    # Deploy Global Config
    global_config = deployers.config_store.load_file(
        "./assets/schemas/global_config.yaml"
    )
    agent_config = deployers.config_store.load_file(
        "./assets/schemas/agent_config.yaml"
    )
    webscraper_config = deployers.config_store.load_file(
        "./assets/schemas/webscraper_config.yaml"
    )
    embeddingsloader_config = deployers.config_store.load_file(
        "./assets/schemas/embeddingsloader_config.yaml"
    )
    example_config = deployers.config_store.load_file(
        "./assets/schemas/example_config.yaml"
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
    deployment_manifest = load_and_validate_schema(
        JobSchema, "./assets/schemas/webscraper_job.yaml"
    )
    # test_deployer(deployers.job_deployer, deployment_manifest)
    # deployers.job_deployer.delete(
    #     name=deployment_manifest.metadata.name,
    #     namespace=deployment_manifest.namespace,
    #     dry_run=DRY_RUN,
    # )

    # Deploy EmbeddingsLoader
    deployment_manifest = load_and_validate_schema(
        JobSchema, "./assets/schemas/embeddingsloader_job.yaml"
    )
    # test_deployer(deployers.job_deployer, deployment_manifest)
    # deployers.job_deployer.delete(
    #     name=deployment_manifest.metadata.name,
    #     namespace=deployment_manifest.namespace,
    #     dry_run=DRY_RUN,
    # )

    # Deploy Agent
    deployment_manifest = load_and_validate_schema(
        DeploymentSchema,
        "./assets/schemas/agent_deployment.yaml",
    )
    # test_deployer(
    #     deployers.deployment_deployer,
    #     deployment_manifest,
    # )

    # test_deployer(deployers.service_deployer, deployment_manifest)
    # deployers.deployment_deployer.delete(
    #     name=deployment_manifest.metadata.name, namespace="default", dry_run=DRY_RUN
    # )
    # deployers.service_deployer.delete(
    #     name=deployment_manifest.metadata.name, namespace="default", dry_run=DRY_RUN
    # )

    # Deploy WebScraper with manifest creators
    _, deployment_manifest = test_manifest_creator(
        "my-web-scraper", "default", "WebScraper", "FlockJob", example_config
    )
    test_deployer(deployers.job_deployer, deployment_manifest)
    deployers.job_deployer.delete(
        name=deployment_manifest.metadata.name,
        namespace=deployment_manifest.namespace,
        dry_run=DRY_RUN,
    )

    # Deploy EmbeddingsLoader with manifest creators
    _, deployment_manifest = test_manifest_creator(
        "embeddings-loader", "default", "EmbeddingsLoader", "FlockJob", example_config
    )
    test_deployer(deployers.job_deployer, deployment_manifest)
    deployers.job_deployer.delete(
        name=deployment_manifest.metadata.name,
        namespace=deployment_manifest.namespace,
        dry_run=DRY_RUN,
    )

    # Deploy Agent with manifest creators
    _, deployment_manifest = test_manifest_creator(
        "my-agent", "default", "Agent", "FlockDeployment", example_config
    )
    test_deployer(deployers.deployment_deployer, deployment_manifest)
    test_deployer(deployers.service_deployer, deployment_manifest)

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


if __name__ == "__main__":
    main()
