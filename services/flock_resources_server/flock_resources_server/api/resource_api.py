"""Flock API"""

from fastapi import APIRouter, Body, Depends, HTTPException
from flock_builder import ResourceBuilder
from flock_resource_store.mongo import ResourceStore
from flock_schemas import SchemaFactory
from pydantic import ValidationError

from flock_resources_server.schemas.resource_details import ResourceDetails
from flock_resources_server.schemas.responses.resource_deleted import ResourceDeleted
from flock_resources_server.schemas.responses.resource_fetched import ResourceFetched
from flock_resources_server.schemas.responses.resource_updated import ResourceUpdated
from flock_resources_server.schemas.responses.resources_fetched import ResourcesFetched


def get_router(
    resource_store: ResourceStore, resource_builder: ResourceBuilder
) -> APIRouter:
    """Get API router"""

    router = APIRouter()
    schema_factory = SchemaFactory()

    @router.get(
        "/resource/{namespace}/{kind}/{name}",
        response_model=ResourceFetched,
    )
    async def get_resource(
        namespace: str,
        kind: str,
        name: str,
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ):
        """Get a resource"""
        try:
            resource_data = resource_store.get(
                namespace=namespace, kind=kind, name=name
            )
            if resource_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"Parameters: {namespace}/{kind}/{name}",
                    ],
                )
            return ResourceFetched(data=resource_data)

        except HTTPException as error:
            raise error
        except ValidationError as error:
            raise HTTPException(
                status_code=500,
                detail=[
                    "Resource is not valid",
                    str(error),
                ],
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get resource",
                    str(error),
                ],
            ) from error

    @router.get("/resource/{namespace}/{category}")
    @router.get("/resource/{namespace}/{kind}")
    async def get_resources(
        kind: str = "",
        category: str = "",
        namespace: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourcesFetched:
        """Get Resources list by namespace and kind"""
        try:
            resource_data = resource_store.get_many(
                namespace=namespace, kind=kind, category=category
            )

            if resource_data is not None and len(resource_data) == 0:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"Parameters: {namespace}/{kind}",
                    ],
                )
            schema_instances = [
                ResourceDetails.validate(item) for item in resource_data  # type: ignore
            ]
            return ResourcesFetched(data=schema_instances)

        except HTTPException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get resource",
                    str(error),
                ],
            ) from error

    @router.post("/resource/validate")
    async def validate_resource(
        resource_data: dict = Body(..., description=""),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceUpdated:
        """Create or update a resource"""

        try:
            schema_instance = schema_factory.get_schema(resource_data["kind"]).validate(
                resource_data
            )
            resource_builder.build_resource(resource_data)
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

        return ResourceUpdated(data=schema_instance)

    @router.put("/resource")
    async def put_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceUpdated:
        """Create or update a resource"""

        try:
            schema_instance = schema_factory.get_schema(resource_data["kind"]).validate(
                resource_data
            )
            resource_builder.build_resource(resource_data)
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

        # store resource
        try:
            resource_store.put(val=schema_instance.dict(by_alias=True))
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceUpdated(data=schema_instance)

    @router.delete(
        "/resource/{namespace}/{category}",
        description="Delete all resources by namespace and category",
    )
    @router.delete(
        "/resource/{namespace}/{kind}",
        description="Delete all resources by namespace and kind",
    )
    async def delete_resources(
        namespace: str = "",
        kind: str = "",
        name: str = "",
        category: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource by namespace, kind and name."""

        try:
            resource_data = resource_store.delete_many(
                namespace=namespace, kind=kind, category=category, name=name
            )
            return ResourceDeleted(
                details=[
                    "Resource deleted",
                    f"Parameters: {namespace}/{kind}/{name}",
                    f"Count: {resource_data.deleted_count}",  # type: ignore
                ],
            )
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to delete resource",
                    str(error),
                ],
            ) from error

    @router.delete(
        "/resource/{namespace}/{kind}/{name}",
        description="Delete a resource by namespace, kind and name",
    )
    async def delete_resource(
        namespace: str = "",
        kind: str = "",
        name: str = "",
        category: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource by namespace, kind and name."""

        try:
            resource_data = resource_store.delete(
                namespace=namespace, kind=kind, category=category, name=name
            )
            return ResourceDeleted(
                details=[
                    "Resource deleted",
                    f"Parameters: {namespace}/{kind}/{name}",
                    f"Count: {resource_data.deleted_count}",  # type: ignore
                ],
            )
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to delete resource",
                    str(error),
                ],
            ) from error

    return router
