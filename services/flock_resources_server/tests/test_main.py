"""Test the API endpoints using FastAPI's TestClient."""

import os

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from flock_common import check_env_vars
from flock_resource_store import ResourceStoreFactory

from flock_resources_server.api.resource_api import ResourceBuilder, get_router

app = FastAPI()

load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
check_env_vars([], [])

resource_store = ResourceStoreFactory.get_resource_store("mongo")
resource_builder = ResourceBuilder(resource_store)

router = get_router(resource_store, resource_builder)
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def test_data():
    """Test data"""
    return [
        {
            "apiVersion": "flock/v1",
            "kind": "Splitter",
            "namespace": "bla",
            "category": "other",
            "created_at": None,
            "updated_at": None,
            "metadata": {
                "name": "test-1",
                "description": "text-splitter",
                "annotations": {},
                "labels": {"app": "my_app"},
            },
            "spec": {
                "vendor": "CharacterTextSplitter",
                "options": {"chunk_size": 30, "chunk_overlap": 0},
            },
        },
        {
            "apiVersion": "flock/v1",
            "kind": "Splitter",
            "namespace": "bla",
            "category": "other",
            "created_at": None,
            "updated_at": None,
            "metadata": {
                "name": "test-2",
                "description": "text-splitter",
                "annotations": {},
                "labels": {"app": "my_app"},
            },
            "spec": {
                "vendor": "CharacterTextSplitter",
                "options": {"chunk_size": 30, "chunk_overlap": 0},
            },
        },
    ]


@pytest.fixture(autouse=True)
def setup_and_cleanup(test_data):
    # Setup - insert test data into resource_store
    for data in test_data:
        resource_store.put(data)

    yield  # This is where the test function gets run

    resource_store.delete_many(
        namespace=test_data[0]["namespace"], kind=test_data[0]["kind"]
    )


def test_get_resource(test_data):
    """Test get_resource endpoint"""

    response = client.get(
        f"/resource/{test_data[0]['namespace']}/{test_data[0]['kind']}/{test_data[0]['metadata']['name']}"
    )
    assert response.status_code == 200
    assert response.json()["data"] == test_data[0]


def test_get_resources(test_data):
    """Test get_resources endpoint"""

    response = client.get(
        f"/resource/{test_data[0]['namespace']}/{test_data[0]['kind']}"
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["name"] == test_data[0]["metadata"]["name"]


def test_put_resource(test_data):
    """Test put_resource endpoint"""

    resource_data = test_data[0]
    response = client.put("/resource", json=resource_data)
    assert response.status_code == 200

    # Check if the resource is created
    response = client.get(
        f"/resource/{resource_data['namespace']}/{resource_data['kind']}/{resource_data['metadata']['name']}"
    )
    assert response.status_code == 200
    assert response.json()["data"] == resource_data


def test_delete_resource(test_data):
    """Test delete_resource endpoint"""

    response = client.delete(
        f"/resource/{test_data[0]['namespace']}/{test_data[0]['kind']}/{test_data[0]['metadata']['name']}"
    )
    assert response.status_code == 200

    # Check if the resource is deleted
    response = client.get(
        f"/resource/{test_data[0]['namespace']}/{test_data[0]['kind']}/{test_data[0]['metadata']['name']}"
    )
    assert response.status_code == 404


def test_delete_resources(test_data):
    """Test delete_resources endpoint"""

    response = client.delete(
        f"/resource/{test_data[0]['namespace']}/{test_data[0]['kind']}"
    )
    assert response.status_code == 200

    # Check if the resources are deleted
    response = client.get(
        f"/resource/{test_data[0]['namespace']}/{test_data[0]['kind']}"
    )
    assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
