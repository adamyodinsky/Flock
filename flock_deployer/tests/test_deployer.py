import yaml
from flock_resource_store import ResourceStoreFactory
from flock_schemas.deployment import DeploymentSchema

from flock_deployer.deployers import DeployerFactory


def test_deployer():
    # create deployer
    deployer = DeployerFactory.get_deployer("k8s")

    # load from yaml file
    path = "../schemas_wip/others/agent_deployment.yaml"
    with open(path, encoding="utf-8") as file:
        deployment_data = yaml.safe_load(file)
        schema_instance = DeploymentSchema.validate(deployment_data)

    deployer.deploy(schema_instance)


test_deployer()
