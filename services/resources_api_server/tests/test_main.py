"""Test the API endpoints using FastAPI's TestClient."""
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.api.resource_api import ResourceBuilder, ResourceStore, get_router

app = FastAPI()
resource_store = MagicMock(spec=ResourceStore)
resource_builder = MagicMock(spec=ResourceBuilder)
router = get_router(resource_store, resource_builder)
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def test_data():
    """Test data"""
    # Add test data here as a list of dictionaries
    return [
        {
            "namespace": "ns1",
            "category": "cat1",
            "kind": "k1",
            "metadata": {"name": "name1"},
        },
        {
            "namespace": "ns2",
            "category": "cat2",
            "kind": "k2",
            "metadata": {"name": "name2"},
        },
    ]


def test_get_resource(test_data):
    """Test get_resource endpoint"""
    # Insert test data into resource_store
    for data in test_data:
        resource_store.put(data)

    response = client.get("/resource/ns1/k1/name1")
    assert response.status_code == 200
    assert response.json()["data"] == test_data[0]

    # Cleanup test data
    resource_store.delete_many(namespace="ns1", kind="k1", name="name1")


def test_get_resources(test_data):
    """Test get_resources endpoint"""
    # Insert test data into resource_store
    for data in test_data:
        resource_store.put(data)

    response = client.get("/resource/ns1/k1")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["metadata"]["name"] == "name1"

    # Cleanup test data
    resource_store.delete_many(namespace="ns1", kind="k1")


def test_put_resource(test_data):
    """Test put_resource endpoint"""

    resource_data = test_data[0]
    response = client.put("/resource", json=resource_data)
    assert response.status_code == 200

    # Check if the resource is created
    response = client.get("/resource/ns1/k1/name1")
    assert response.status_code == 200
    assert response.json()["data"] == resource_data

    # Cleanup test data
    resource_store.delete(namespace="ns1", kind="k1", name="name1")


def test_delete_resource(test_data):
    """Test delete_resource endpoint"""
    # Insert test data into resource_store
    for data in test_data:
        resource_store.put(data)

    response = client.delete("/resource/ns1/k1/name1")
    assert response.status_code == 200

    # Check if the resource is deleted
    response = client.get("/resource/ns1/k1/name1")
    assert response.status_code == 404

    # Cleanup test data
    resource_store.delete_many(namespace="ns1", kind="k1")


def test_delete_resources(test_data):
    """Test delete_resources endpoint"""
    # Insert test data into resource_store
    for data in test_data:
        resource_store.put(data)

    response = client.delete("/resource/ns1/k1")
    assert response.status_code == 200

    # Check if the resources are deleted
    response = client.get("/resource/ns1/k1")
    assert response.status_code == 404

    # # Cleanup test data
    # resource
