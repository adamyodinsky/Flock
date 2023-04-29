from fastapi import (  # Cookie,; Depends,; Header,; Query,; Response,; Security,; status,
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
)
from flock_models.builder import ResourceBuilder
from flock_resource_store import ResourceStore
from pydantic import ValidationError


async def put_resource(
    namespace: str = Path(..., description="Namespace of resource"),
    kind: str = Path(..., description="Kind of resource"),
    name: str = Path(..., description="Name of a resource"),
    resource_data: dict = Body(..., description=""),
    resource_store: ResourceStore = Depends(lambda: resource_store),
):
    """Create or update a resource"""

    try:
        assert namespace == resource_data["namespace"]
        assert kind == resource_data["kind"]
        assert name == resource_data["metadata"]["name"]
    except AssertionError:
        return ResourceBadRequest(
            details=[
                "Resource data does not match parameters",
                f"Parameters: {namespace}/{kind}/{name}",
                f"Schema: {resource_data['namespace']}/{resource_data['kind']}/{resource_data['metadata']['name']}",
            ],
        )

    try:
        # validate resource building
        resource_builder.build_resource(resource_data)
    except ValidationError as error:
        return ResourceBadRequest(
            details=["Failed to build resource", str(error)],
        )
    except Exception as error:  # pylint: disable=broad-except
        return InternalServerError(
            details=["Failed to build resource", str(error)],
        )

    # store resource
    try:
        resource_store.put(
            key=f"{namespace}/{kind}/{name}",
            val=resource_data,
        )
    except Exception as error:  # pylint: disable=broad-except
        return InternalServerError(
            details=[
                "Failed to store resource",
                str(error),
            ],
        )
