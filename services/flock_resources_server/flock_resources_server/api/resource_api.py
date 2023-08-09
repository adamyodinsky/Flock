"""Flock API"""

from fastapi import APIRouter, Body, Depends, HTTPException
from flock_builder import ResourceBuilder
from flock_resource_store.mongo import ResourceStore
from flock_schema_store import SchemaStore
from flock_schemas import SchemaFactory
from pydantic import ValidationError

from flock_resources_server.schemas.resource_details import ResourceDetails
from flock_resources_server.schemas.responses.resource_deleted import ResourceDeleted
from flock_resources_server.schemas.responses.resource_fetched import (
    KindsFetched,
    ResourceFetched,
    SchemasFetched,
)
from flock_resources_server.schemas.responses.resource_updated import ResourceUpdated
from flock_resources_server.schemas.responses.resources_fetched import ResourcesFetched


def get_router(
    resource_store: ResourceStore,
    resource_builder: ResourceBuilder,
    schema_store: SchemaStore,
    prefix: str,
) -> APIRouter:
    """Get API router"""

    router = APIRouter()
    schema_factory = SchemaFactory()

    @router.get("/")
    @router.get("/health")
    @router.head("/health")
    @router.get(f"/{prefix}/health")
    async def health(
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ):
        """Health check"""

        healthy = resource_store.health_check()

        if healthy:
            return {"status": "OK"}
        raise HTTPException(
            status_code=500,
            detail=[
                "Resource store is not healthy",
            ],
        )

    @router.get("/resource")
    @router.get("/resource/{id}")
    async def get_resource(
        namespace: str = "",
        kind: str = "",
        category: str = "",
        name: str = "",
        id: str = "",
        tool: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceFetched:
        """Get a resource"""
        try:
            resource_data = resource_store.get(
                namespace=namespace,
                kind=kind,
                category=category,
                name=name,
                id=id,
                tool=tool,
            )

            if resource_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"namespace: {namespace}",
                        f"kind: {kind}",
                        f"category: {category}",
                        f"name: {name}",
                    ],
                )

            return ResourceFetched(data=resource_data)

        except HTTPException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get resource",
                    str(error),
                ],
            ) from error

    @router.get("/resources")
    async def get_resources(
        kind: str = "",
        category: str = "",
        namespace: str = "",
        tool: str = "",
        page: int = 1,
        page_size: int = 50,
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourcesFetched:
        """Get Resources list by namespace and kind"""
        try:
            resource_data = resource_store.get_many(
                namespace=namespace,
                kind=kind,
                category=category,
                tool=tool,
                page=page,
                page_size=page_size,
            )

            fetched_resources = [
                ResourceDetails.validate(item) for item in resource_data
            ]
            return ResourcesFetched(data=fetched_resources)

        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get resource",
                    f"namespace: {namespace}",
                    f"kind: {kind}",
                    f"category: {category}",
                    str(error),
                ],
            ) from error

    @router.post("/resource")
    async def create_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceUpdated:
        """Create or update a resource.

        If the resource already exists, an error will be returned.
        """

        try:
            name: str = resource_data["metadata"]["name"]
            namespace: str = resource_data["namespace"]
            kind: str = resource_data["kind"]

            if (
                resource_store.get(namespace=namespace, kind=kind, name=name)
                is not None
            ):
                raise HTTPException(
                    status_code=422,
                    detail=[
                        "Resource already exists",
                        f"namespace: {namespace}",
                        f"kind: {kind}",
                        f"name: {name}",
                    ],
                )
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(
                status_code=422,
                detail=["Failed to build resource", str(error)],
            ) from error

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
                status_code=400,
                detail=["Failed to build resource", str(error)],
            ) from error

        # store resource
        try:
            resource_store.put(val=schema_instance.dict(by_alias=True))
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceUpdated(data=schema_instance)

    @router.put("/resource/{id}")
    async def put_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
        id: str = "",
    ) -> ResourceUpdated:
        """Create or update a resource.

        If the resource already exists, it will be updated. Otherwise, an error will be returned.
        """
        fetched_resource = {}
        try:
            fetched_resource = resource_store.get(id=id)
            if fetched_resource is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"id: {id}",
                    ],
                )
        except HTTPException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to fetch resource",
                    str(error),
                ],
            ) from error

        resource_data["id"] = fetched_resource["id"]

        try:
            schema_instance = schema_factory.get_schema(resource_data["kind"]).validate(
                resource_data
            )
            resource_builder.build_resource(resource_data)
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=["Failed to build resource", str(error)],
            ) from error

        # store resource
        try:
            resource_store.put(val=schema_instance.dict(by_alias=True))
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceUpdated(data=schema_instance)

    @router.delete(
        "/resource",
        description="Delete resource",
    )
    @router.delete(
        "/resource/{id}",
        description="Delete resource",
    )
    async def delete_resource(
        namespace: str = "",
        kind: str = "",
        category: str = "",
        name: str = "",
        id: str = "",
        tool: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource."""

        try:
            resource_data = resource_store.delete_many(
                namespace=namespace,
                kind=kind,
                category=category,
                name=name,
                id=id,
                tool=tool,
            )
            return ResourceDeleted(
                details=[
                    "Resource deleted",
                    f"Parameters: namespace={namespace}, kind={kind}, category={category}, name={name}, id={id}",
                    f"Count: {resource_data.deleted_count}",  # type: ignore
                ],
            )
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to delete resource",
                    str(error),
                ],
            ) from error

    @router.post("/resource/validate")
    async def validate_resource(
        resource_data: dict = Body(..., description=""),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceUpdated:
        """Resource validation only

        This endpoint does not store the resource. It is used to validate the resource only.
        """

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

    @router.get("/schema/{kind}")
    async def get_schema(
        schema_store: SchemaStore = Depends(lambda: schema_store), kind: str = ""
    ):
        """Get schema for kind"""
        try:
            schema_data = schema_store.get(kind=kind)

            if schema_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Schema not found",
                        f"kind: {kind}",
                    ],
                )

            return ResourceFetched(data=schema_data)

        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get schema",
                    str(error),
                ],
            ) from error

    @router.get("/schemas")
    async def get_schemas(
        schema_store: SchemaStore = Depends(lambda: schema_store),
    ) -> SchemasFetched:
        """Get all schemas"""

        try:
            schemas_data = schema_store.get_many()

            return SchemasFetched(data=schemas_data)

        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get schemas",
                    str(error),
                ],
            ) from error

    @router.get("/kinds")
    async def get_kinds(
        schema_store: SchemaStore = Depends(lambda: schema_store),
    ) -> KindsFetched:
        """Get all kinds"""
        try:
            kinds_data = schema_store.get_kinds()

            return KindsFetched(data=kinds_data)

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get kinds",
                    str(error),
                ],
            ) from error

    return router
