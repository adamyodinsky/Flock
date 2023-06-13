import os

from fastapi import APIRouter, Body, Depends, HTTPException
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from flock_schemas.factory import SchemaFactory
from pydantic import ValidationError

from flock_deployer.deployer import DeployerFactory
from flock_deployer.deployer.base import BaseDeployers
from flock_deployer.schemas import ResourceCreated
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.request import DeploymentRequest

resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.environ.get("FLOCK_RESOURCE_STORE_TYPE", "mongo"),
    db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
    host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
    port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
    username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
    password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
)

schema_factory = SchemaFactory()


secret_store = SecretStoreFactory.get_secret_store("vault")
deployer = DeployerFactory.get_deployer(
    deployer_type="k8s",
    secret_store=secret_store,
    resource_store=resource_store,
)


def get_router(deployers: BaseDeployers) -> APIRouter:
    """Get API router"""

    router = APIRouter()

    @router.post("/deploy")
    async def deploy(
        data: DeploymentRequest = Body(..., description=""),
        deployers: BaseDeployers = Depends(lambda: deployers),
    ) -> ResourceCreated:
        """Deploy

        Deploy a resource to the target cluster.

        Args:
            data (DeploymentRequest): Deployment request
            deployers (BaseDeployers): Deployers

        Raises:
            HTTPException: Failed to build resource
            HTTPException: Failed to store resource

        Returns:
            ResourceCreated: Resource created
        """

        try:
            target_manifest = deployers.get_target_manifest(
                name=data.resource_name,
                namespace=data.resource_namespace,
                kind=data.resource_kind,
            )

            creator = deployers.get_creator(data.resource_kind)
            deployment_schema: DeploymentSchema = creator(
                data.deployment_name, data.deployment_namespace, target_manifest
            )

        except ValidationError as error:
            raise HTTPException(
                status_code=400,
                detail=["Failed to build resource", str(error)],
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=["Failed to build resource", str(error)],
            ) from error

        try:
            if data.resource_kind == "Agent":
                deployers.service_deployer.deploy(
                    deployment_schema, target_manifest, dry_run=False
                )
                deployers.deployment_deployer.deploy(
                    deployment_schema, target_manifest, dry_run=False
                )
            else:
                deployers.job_deployer.deploy(
                    deployment_schema, target_manifest, dry_run=False
                )

        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceCreated(data=deployment_schema)

    return router
