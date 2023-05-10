import yaml
from flock_resource_store import ResourceStoreFactory
from flock_schemas import SchemasFactory
from flock_schemas.deployment import DeploymentSchema

from flock_deployer.deployers import DeployerFactory


def test_deployer():
    """Test deployer from a schema manifest file."""

    # create deployer
    deployer = DeployerFactory.get_deployer("k8s")
    resource_store = ResourceStoreFactory.get_resource_store()

    # load from yaml file
    path = "../schemas_wip/others/agent_deployment.yaml"
    with open(path, encoding="utf-8") as file:
        deployment_data = yaml.safe_load(file)

    schema_instance = DeploymentSchema.validate(deployment_data)
    target_manifest = resource_store.get(
        name=schema_instance.spec.targetResource.name,
        kind=schema_instance.spec.targetResource.kind,
        namespace=schema_instance.spec.targetResource.namespace,  # type: ignore
    )
    schema_cls = SchemasFactory.get_schema(target_manifest["kind"])
    target_manifest = schema_cls.validate(target_manifest)
    # deployer.dry_deploy(schema_instance, target_manifest)
    deployer.deploy(schema_instance, target_manifest)


test_deployer()
