from fastapi import APIRouter, Body, Depends, HTTPException
from flock_schemas.deployment import DeploymentSchema
from pydantic import ValidationError

from flock_deployer.deployers.base import BaseDeployer
from flock_deployer.schemas import ResourceCreated


def get_router(deployer: BaseDeployer) -> APIRouter:
    """Get API router"""

    router = APIRouter()

    @router.post("/deploy")
    async def deploy(
        resource_data: dict = Body(..., description=""),
        deployer: BaseDeployer = Depends(lambda: deployer),
    ) -> ResourceCreated:
        """Deploy"""

        # validate schema
        try:
            schema_instance = DeploymentSchema.validate(resource_data)
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

        # deploy
        try:
            deployer.deploy(schema_instance)
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceCreated(data=schema_instance)

    return router
