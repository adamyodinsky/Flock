import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import ValidationError

from flock_deployer.deployer.base import BaseDeployers
from flock_deployer.schemas import DeploymentConfigSchema, DeploymentSchema
from flock_deployer.schemas.request import (
    ConfigRequest,
    DeleteRequest,
    DeploymentRequest,
)
from flock_deployer.schemas.response import (
    ConfigCreated,
    HealthResponse,
    ResourceCreated,
    ResourceDeleted,
)


def get_router(deployers: BaseDeployers) -> APIRouter:
    """Get API router"""

    logging.info("Creating API router")
    router = APIRouter()

    @router.get("/health")
    @router.get("/")
    async def health_endpoint(
        deployers: BaseDeployers = Depends(lambda: deployers),
    ) -> HealthResponse:
        """Health endpoint

        Check the health of the deployer.

        Args:


        Returns:
            dict: Health status

        """

        logging.info("Checking health")
        resource_store_health = deployers.resource_store.health_check()
        secret_store_health = deployers.secret_store.health_check()
        config_store_health = deployers.config_store.health_check()

        return HealthResponse(
            status="OK"
            if all([resource_store_health, secret_store_health, config_store_health])
            else "ERROR",
            stores={
                "resource_store": "OK" if resource_store_health else "ERROR",
                "secret_store": "OK" if secret_store_health else "ERROR",
                "config_store": "OK" if config_store_health else "ERROR",
            },
        )

    @router.put("/deployment")
    async def put_deployment(
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
            logging.debug("Fetching %s %s", data.resource_name, data.resource_kind)
            target_manifest = deployers.get_target_manifest(
                name=data.resource_name,
                namespace=data.resource_namespace,
                kind=data.resource_kind,
            )

            logging.debug(
                "Creating deployment schema", data.resource_name, data.resource_kind
            )
            creator = deployers.get_creator(data.deployment_kind)
            deployment_schema = creator(
                name=data.deployment_name,
                namespace=data.deployment_namespace,
                target_manifest=target_manifest,
                config=data.config,
                schedule=data.schedule,
            )
        except ValidationError as error:
            logging.error(
                "Failed to deploy %s %s", data.resource_name, data.resource_kind
            )
            logging.error(error)
            raise HTTPException(
                status_code=400,
                detail=["Failed to deploy", str(error)],
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            logging.error(
                "Failed to deploy %s %s", data.resource_name, data.resource_kind
            )
            logging.error(error)
            raise HTTPException(
                status_code=500,
                detail=["Failed to deploy", str(error)],
            ) from error

        logging.info("Deploying resource %s %s", data.resource_name, data.resource_kind)
        try:
            match data.deployment_kind:
                case "FlockDeployment":
                    deployers.service_deployer.deploy(
                        deployment_schema, target_manifest, dry_run=data.dry_run
                    )
                    deployers.deployment_deployer.deploy(
                        deployment_schema, target_manifest, dry_run=data.dry_run
                    )
                case "FlockJob":
                    deployers.job_deployer.deploy(
                        deployment_schema, target_manifest, dry_run=data.dry_run
                    )
                case "FlockCronJob":
                    deployers.cronjob_deployer.deploy(
                        deployment_schema, target_manifest, dry_run=data.dry_run
                    )
                case _:
                    raise HTTPException(
                        status_code=400,
                        detail=["Failed to store resource", "Invalid deployment kind"],
                    )

        except Exception as error:  # pylint: disable=broad-except
            logging.error("Failed to deploy %s", data.resource_name)
            logging.error(error)
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to deploy",
                    str(error),
                ],
            ) from error

        return ResourceCreated(data=deployment_schema)

    @router.delete("/deployment")
    async def delete_deployment(
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
            match data.deployment_kind:
                case "FlockDeployment":
                    deployers.service_deployer.delete(
                        name=data.deployment_name,
                        namespace=data.deployment_namespace,
                        dry_run=data.dry_run,
                    )
                    deployers.deployment_deployer.delete(
                        name=data.deployment_name,
                        namespace=data.deployment_namespace,
                        dry_run=data.dry_run,
                    )
                case "FlockJob":
                    deployers.job_deployer.delete(
                        name=data.deployment_name,
                        namespace=data.deployment_namespace,
                        dry_run=data.dry_run,
                    )
                case "FlockCronJob":
                    deployers.cronjob_deployer.delete(
                        name=data.deployment_name,
                        namespace=data.deployment_namespace,
                        dry_run=data.dry_run,
                    )

        except Exception as error:  # pylint: disable=broad-except
            logging.error("Failed to delete deployment %s", data.deployment_name)
            logging.error(error)
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceDeleted()

    @router.put("/config")
    async def create_config(
        data: ConfigRequest = Body(..., description=""),
        deployers: BaseDeployers = Depends(lambda: deployers),
    ) -> ConfigCreated:
        """
        Create config

        Args:
            data (ConfigRequest): Config request
            deployers (BaseDeployers): Deployers

        Raises:
            HTTPException: Failed to store config

        Returns:
            ResourceCreated: Resource created
        """

        logging.info("Creating config %s", data.config.metadata.name)
        try:
            deployers.config_store.put(data.config.dict())
        except Exception as error:  # pylint: disable=broad-except
            logging.error("Failed to store config %s", data.config.metadata.name)
            logging.error(error)
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store config",
                    str(error),
                ],
            ) from error

        return ConfigCreated(data=data.config)

    @router.get("/config/{name}")
    async def get_config(
        name: str,
        deployers: BaseDeployers = Depends(lambda: deployers),
    ) -> DeploymentConfigSchema:
        """
        Get config

        Args:
            name (str): Config name
            deployers (BaseDeployers): Deployers

        Raises:
            HTTPException: Failed to get config

        Returns:
            Config: Config
        """

        logging.info("Getting config %s", name)
        try:
            config = deployers.config_store.get(name=name)
            config = DeploymentConfigSchema.validate(config)
            return config
        except Exception as error:
            logging.error("Failed to get config %s", name)
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get config",
                    str(error),
                ],
            ) from error

    @router.delete("/config/{name}")
    async def delete_config(
        name: str,
        deployers: BaseDeployers = Depends(lambda: deployers),
    ) -> ResourceDeleted:
        """
        Delete config

        Args:
            name (str): Config name
            deployers (BaseDeployers): Deployers

        Raises:
            HTTPException: Failed to delete config

        Returns:
            Config: Config
        """
        logging.info("Deleting config %s", name)
        try:
            deployers.config_store.delete(name=name)
            return ResourceDeleted()
        except Exception as error:
            logging.error("Failed to delete config %s", name)
            logging.error(error)
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to delete config",
                    str(error),
                ],
            ) from error

    return router
