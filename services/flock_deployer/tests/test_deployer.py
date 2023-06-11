import time

import yaml
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from flock_schemas.factory import SchemaFactory

from flock_deployer.deployer import DeployerFactory
from flock_deployer.manifest_creator.creator import ManifestCreator
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.job import JobSchema

schema_factory = SchemaFactory()
deployment_example = {
    "apiVersion": "flock/v1",
    "kind": "Agent",
    "namespace": "default",
    "metadata": {
        "name": "my-agent",
        "description": "A Q&A agent for internal projects",
        "labels": {"app": "my_app"},
    },
    "spec": {
        "vendor": "conversational-react-description",
        "options": {"verbose": True},
        "dependencies": [
            {"kind": "LLMChat", "name": "my-openai-llm-gpt4", "namespace": "default"}
        ],
        "tools": [
            {
                "kind": "LoadTool",
                "name": "my-google-search-gpt4",
                "namespace": "default",
            }
        ],
    },
}


def test_deployer(dry_run: bool = True):
    """Test deployer from a schema manifest file."""

    # create deployer

    secret_store = SecretStoreFactory.get_secret_store("vault")
    resource_store = ResourceStoreFactory.get_resource_store()
    deployer = DeployerFactory.get_deployer(
        deployer_type="k8s",
        secret_store=secret_store,
    )

    # load from yaml file
    path = "./assets/schemas/agent_deployment.yaml"
    with open(path, encoding="utf-8") as file:
        deployment_data = yaml.safe_load(file)

    deployment_manifest = DeploymentSchema.validate(deployment_data)
    target_manifest = resource_store.get(
        name=deployment_manifest.spec.targetResource.name,
        kind=deployment_manifest.spec.targetResource.kind,
        namespace=deployment_manifest.spec.targetResource.namespace,  # type: ignore
    )
    schema_cls = schema_factory.get_schema(target_manifest["kind"])
    target_manifest = schema_cls.validate(target_manifest)
    deployer.deployment_deployer.deploy(
        deployment_manifest, target_manifest, dry_run=dry_run
    )
    deployer.service_deployer.deploy(
        deployment_manifest, target_manifest, dry_run=dry_run
    )
    deployer.deployment_deployer.delete(
        deployment_manifest, target_manifest, dry_run=dry_run
    )
    deployer.service_deployer.delete(
        deployment_manifest, target_manifest, dry_run=dry_run
    )


def test_job(dry_run: bool = True):
    """Test deployer from a schema manifest file."""

    # create deployer

    secret_store = SecretStoreFactory.get_secret_store("vault")
    resource_store = ResourceStoreFactory.get_resource_store()
    deployer = DeployerFactory.get_deployer(
        deployer_type="k8s",
        secret_store=secret_store,
    )

    # load from yaml file
    path = "./assets/schemas/embeddings_loader_job.yaml"
    with open(path, encoding="utf-8") as file:
        job_data = yaml.safe_load(file)

    job_manifest = JobSchema.validate(job_data)
    target_manifest = resource_store.get(
        name=job_manifest.spec.targetResource.name,
        kind=job_manifest.spec.targetResource.kind,
        namespace=job_manifest.spec.targetResource.namespace,  # type: ignore
    )
    target_schema_cls = schema_factory.get_schema(target_manifest["kind"])
    target_manifest = target_schema_cls.validate(target_manifest)
    deployer.job_deployer.deploy(job_manifest, target_manifest, dry_run=dry_run)
    # deployer.job_deployer.delete(job_manifest, target_manifest, dry_run=True)


def test_manifest_creator():
    """Test manifest creator."""

    manifest_creator = ManifestCreator()

    manifest = manifest_creator.create_deployment(
        name="test-agent",
        namespace="default",
        target_manifest=schema_factory.get_schema(deployment_example["kind"]).validate(
            deployment_example
        ),
    )

    print(manifest)


def test_manifest_creator_and_deployer(dry_run: bool = True):
    """Test manifest creator and deployer."""

    secret_store = SecretStoreFactory.get_secret_store("vault")
    resource_store = ResourceStoreFactory.get_resource_store()
    deployer = DeployerFactory.get_deployer(
        deployer_type="k8s",
        secret_store=secret_store,
    )
    manifest_creator = ManifestCreator()
    target_kind = "Agent"  # get from user input
    target_name = "my-agent"  # get from user input
    target_namespace = "default"  # get from user input
    target_manifest = resource_store.get(
        name=target_name, kind=target_kind, namespace=target_namespace
    )
    target_manifest = schema_factory.get_schema(deployment_example["kind"]).validate(
        target_manifest
    )

    deployment_manifest = manifest_creator.create_deployment(
        name="test-agent",
        namespace="default",
        target_manifest=target_manifest,
    )

    deployer.deployment_deployer.deploy(
        deployment_manifest, target_manifest, dry_run=dry_run
    )
    deployer.service_deployer.deploy(
        deployment_manifest, target_manifest, dry_run=dry_run
    )

    time.sleep(3)

    deployer.deployment_deployer.delete(
        deployment_manifest.metadata.name,
        deployment_manifest.namespace,
        dry_run=dry_run,
    )
    deployer.service_deployer.delete(
        deployment_manifest.metadata.name,
        deployment_manifest.namespace,
        dry_run=dry_run,
    )


DRY_RUN = False

# test_job(DRY_RUN)
test_deployer(DRY_RUN)
# test_manifest_creator()
# test_manifest_creator_and_deployer(DRY_RUN)
