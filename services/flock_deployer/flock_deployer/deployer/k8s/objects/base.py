"""Kubernetes Deployment controller."""

import abc

from flock_schemas.base import BaseFlockSchema
from kubernetes import client

from flock_deployer.schemas.deployment import DeploymentSchema


def merge_dicts_or_pydantic(ob1, ob2):
    """Merge two dictionaries or pydantic objects."""
    ob1 = dict(ob1)
    ob2 = dict(ob2)

    return {**ob1, **ob2}


class K8sResource(metaclass=abc.ABCMeta):
    """Kubernetes Resource object."""

    def __init__(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        """Initialize the resource."""

        if target_manifest is not NotImplemented:
            manifest.spec.targetResource.options = merge_dicts_or_pydantic(
                target_manifest.spec.options, manifest.spec.targetResource.options
            )

            self.target_manifest = target_manifest
        else:
            self.target_manifest = None

        self.metadata = client.V1ObjectMeta(
            name=manifest.metadata.name,
            namespace=manifest.namespace,
            labels=manifest.metadata.labels,
        )

        self.namespace = manifest.namespace
        self.manifest = manifest
        self.rendered_manifest = None
