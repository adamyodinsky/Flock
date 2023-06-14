import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import ValidationError

from flock_deployer.deployer.base import BaseDeployers
from flock_deployer.schemas import ResourceCreated, ResourceDeleted
from flock_deployer.schemas.deployment import DeploymentSchema
from flock_deployer.schemas.request import DeleteRequest, DeploymentRequest


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
        logging.info("Creating resource objects%s", data.resource_name)
        try:
            target_manifest = deployers.get_target_manifest(
                name=data.resource_name,
                namespace=data.resource_namespace,
                kind=data.resource_kind,
            )

            creator = deployers.get_creator(data.deployment_kind)
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

        logging.info("Deploying resource %s", data.resource_name)
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

    @router.post("/delete")
    async def delete(
        data: DeleteRequest = Body(..., description=""),
        deployers: BaseDeployers = Depends(lambda: deployers),
    ) -> ResourceDeleted:
        """Delete

        Delete a resource from the target cluster.

        Args:
            data (DeleteRequest): Delete request
            deployers (BaseDeployers): Deployers

        Raises:
            HTTPException: Failed to build resource
            HTTPException: Failed to store resource

        Returns:
            ResourceDeleted: Resource deleted
        """

        logging.info("Deleting resource %s", data.deployment_name)
        try:
            if data.resource_kind == "Agent":
                deployers.service_deployer.delete(
                    name=data.deployment_name,
                    namespace=data.deployment_namespace,
                    dry_run=False,
                )
                deployers.deployment_deployer.delete(
                    name=data.deployment_name,
                    namespace=data.deployment_namespace,
                    dry_run=False,
                )
            else:
                deployers.job_deployer.delete(
                    name=data.deployment_name,
                    namespace=data.deployment_namespace,
                    dry_run=False,
                )

        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceDeleted()

    return router
