""" Test """

import yaml
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from flock_schemas.factory import SchemaFactory

from flock_deployer.deployer import DeployerFactory
from flock_deployer.manifest_creator.creator import ManifestCreator
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.job import JobSchema

manifest_creator_target_manifest = {
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


def setup_deployer():
    secret_store = SecretStoreFactory.get_secret_store("vault")
    return DeployerFactory.get_deployer(
        deployer_type="k8s",
        secret_store=secret_store,
    )


schema_factory = SchemaFactory()
resource_store = ResourceStoreFactory.get_resource_store()
DRY_RUN = False


def load_and_validate_schema(schema_class, yaml_path):
    with open(yaml_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return schema_class.validate(data)


def process_manifest(deployer, data, target_manifest, dry_run):
    deployer.deploy(data, target_manifest, dry_run=dry_run)


def test_deployer(deployer, yaml_path, schema_cls, dry_run=DRY_RUN):
    data = load_and_validate_schema(schema_cls, yaml_path)
    target_manifest = resource_store.get(
        name=data.spec.targetResource.name,
        kind=data.spec.targetResource.kind,
        namespace=data.spec.targetResource.namespace,
    )
    target_schema_cls = schema_factory.get_schema(target_manifest["kind"])
    target_manifest = target_schema_cls.validate(target_manifest)

    process_manifest(deployer, data, target_manifest, dry_run)


def test_manifest_creator(
    target_name, target_namespace, target_kind, creator_function
) -> tuple:
    target_manifest = resource_store.get(
        name=target_name, kind=target_kind, namespace=target_namespace
    )
    deployment_manifest = creator_function(
        name=target_name,
        namespace=target_namespace,
        target_manifest=schema_factory.get_schema(target_kind).validate(
            target_manifest
        ),
    )
    return target_manifest, deployment_manifest


def test_manifest_creator_and_deployer(
    target_kind, target_name, target_namespace, creator_function, dry_run=DRY_RUN
):
    target_manifest, deployment_manifest = creator_function(
        target_name, target_namespace, target_kind
    )

    deployer = setup_deployer()

    process_manifest(
        deployer.deployment_deployer, deployment_manifest, target_manifest, dry_run
    )


def delete(target_name, target_namespace, deployer, dry_run=DRY_RUN):
    deployer.delete(
        name=target_name,
        namespace=target_namespace,
        dry_run=dry_run,
    )


def main():
    deployer = setup_deployer()
    manifest_creator = ManifestCreator()
    manifest_creator_deployment = manifest_creator.create_deployment
    manifest_creator_job = manifest_creator.create_job

    test_manifest_creator("my-agent", "default", "Agent", manifest_creator_deployment)
    test_manifest_creator(
        "my-embedding-data-loader", "default", "EmbeddingsLoader", manifest_creator_job
    )

    # Deploy Job
    test_deployer(
        deployer.job_deployer,
        "./assets/schemas/embeddings_loader_job.yaml",
        JobSchema,
    )
    deployer.job_deployer.delete(
        name="my-embedding-data-loader", namespace="default", dry_run=DRY_RUN
    )

    # # Deploy Deployment
    # test_deployer(
    #     deployer.deployment_deployer,
    #     "./assets/schemas/agent_deployment.yaml",
    #     DeploymentSchema,
    # )
    # test_deployer(
    #     deployer.service_deployer,
    #     "./assets/schemas/agent_deployment.yaml",
    #     DeploymentSchema,
    # )
    # deployer.deployment_deployer.delete(
    #     name="my-agent", namespace="default", dry_run=DRY_RUN
    # )
    # deployer.service_deployer.delete(
    #     name="my-agent", namespace="default", dry_run=DRY_RUN
    # )

    # # Manifest creator deployment
    # test_manifest_creator_and_deployer(
    #     "Agent", "my-agent", "default", manifest_creator_deployment
    # )
    # deployer.deployment_deployer.delete(
    #     name="my-agent", namespace="default", dry_run=DRY_RUN
    # )

    # # Manifest creator job
    # test_manifest_creator_and_deployer(
    #     "EmbeddingsLoader", " my-embedding-data-loader", "default", manifest_creator_job
    # )
    # deployer.job_deployer.delete(
    #     name="my-embedding-data-loader", namespace="default", dry_run=DRY_RUN
    # )


if __name__ == "__main__":
    main()
