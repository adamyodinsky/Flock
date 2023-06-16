""" Test """

import os

import yaml
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from flock_schemas.factory import SchemaFactory

from flock_deployer.deployer import DeployerFactory
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.job import JobSchema

resource_store = ResourceStoreFactory.get_resource_store()
secret_store = SecretStoreFactory.get_secret_store("vault")


def setup_deployers():
    return DeployerFactory.get_deployer(
        deployer_type=os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"),
        secret_store=secret_store,
        resource_store=resource_store,
    )


schema_factory = SchemaFactory()
deployers = setup_deployers()
DRY_RUN = False


def load_and_validate_schema(schema_class, yaml_path):
    with open(yaml_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return schema_class.validate(data)


def process_manifest(deployer, data, target_manifest, dry_run):
    deployer.deploy(data, target_manifest, dry_run=dry_run)


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
    target_name, target_namespace, target_kind, deployment_kind
) -> tuple:
    target_manifest = resource_store.get(
        name=target_name, kind=target_kind, namespace=target_namespace
    )
    deployment_manifest = deployers.get_creator(deployment_kind)(
        name=target_name,
        namespace=target_namespace,
        target_manifest=schema_factory.get_schema(target_kind).validate(
            target_manifest
        ),
    )
    return target_manifest, deployment_manifest


def delete(target_name, target_namespace, deployer, dry_run=DRY_RUN):
    deployer.delete(
        name=target_name,
        namespace=target_namespace,
        dry_run=dry_run,
    )


# TODO: fix this tests, match to the refactored code
def main():
    # deployment_manifest = load_and_validate_schema(
    #     JobSchema, "./assets/schemas/web_scraper_job.yaml"
    # )
    # test_deployer(deployers.job_deployer, deployment_manifest)

    # deployment_manifest = load_and_validate_schema(
    #     JobSchema, "./assets/schemas/embeddings_loader_job.yaml"
    # )
    # test_deployer(deployers.job_deployer, deployment_manifest)

    # deployers.job_deployer.delete(
    #     name="web-scraper", namespace="default", dry_run=DRY_RUN
    # )
    # deployers.job_deployer.delete(
    #     name="embeddings-loader", namespace="default", dry_run=DRY_RUN
    # )

    # # Deploy Deployment
    # deployment_manifest = load_and_validate_schema(
    #     DeploymentSchema,
    #     "./assets/schemas/agent_deployment.yaml",
    # )
    # test_deployer(
    #     deployers.deployment_deployer,
    #     deployment_manifest,
    # )

    # test_deployer(deployers.service_deployer, deployment_manifest)
    # deployers.deployment_deployer.delete(
    #     name="my-agent", namespace="default", dry_run=DRY_RUN
    # )
    # deployers.service_deployer.delete(
    #     name="my-agent", namespace="default", dry_run=DRY_RUN
    # )

    # Deploy Job with manifest creators
    _, deployment_manifest = test_manifest_creator(
        "my-web-scraper", "default", "WebScraper", "FlockJob"
    )
    test_deployer(deployers.job_deployer, deployment_manifest)
    deployers.job_deployer.delete(
        name="my-web-scraper", namespace="default", dry_run=DRY_RUN
    )

    _, deployment_manifest = test_manifest_creator(
        "my-embedding-data-loader", "default", "EmbeddingsLoader", "FlockJob"
    )
    test_deployer(deployers.job_deployer, deployment_manifest)
    deployers.job_deployer.delete(
        name="my-embedding-data-loader", namespace="default", dry_run=DRY_RUN
    )

    _, deployment_manifest = test_manifest_creator(
        "my-agent", "default", "Agent", "FlockDeployment"
    )
    test_deployer(deployers.deployment_deployer, deployment_manifest)

    deployers.deployment_deployer.delete(
        name="my-agent", namespace="default", dry_run=DRY_RUN
    )
    deployers.service_deployer.delete(
        name="my-agent", namespace="default", dry_run=DRY_RUN
    )


if __name__ == "__main__":
    main()
