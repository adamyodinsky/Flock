# coding: utf-8

from fastapi.testclient import TestClient


from server.models.internal_server_error import InternalServerError1  # noqa: F401
from server.models.resource_bad_request import ResourceBadRequest1  # noqa: F401
from server.models.resource_fetched import ResourceFetched  # noqa: F401
from server.models.resource_not_found import ResourceNotFound1  # noqa: F401
from server.models.resources_fetched import ResourcesFetched  # noqa: F401


def test_get_resource(client: TestClient):
    """Test case for get_resource

    get-resource
    """

    headers = {}
    response = client.request(
        "GET",
        "/resource/{namespace}/{kind}/{name}".format(
            namespace="namespace_example", kind="kind_example", name="name_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_resource_namespace_kind(client: TestClient):
    """Test case for get_resource_namespace_kind

    get-resource-namespace-kind
    """

    headers = {}
    response = client.request(
        "GET",
        "/resource/{namespace}/{kind}".format(
            namespace="namespace_example", kind="kind_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
