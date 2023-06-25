"""Kubernetes Deployment controller."""

import abc

from flock_schemas.base import BaseResourceSchema
from kubernetes import client

from flock_deployer.schemas.deployment import DeploymentSchema


class K8sResource(metaclass=abc.ABCMeta):
    """Kubernetes Resource object."""

    def merge_dicts_or_pydantic(self, ob1, ob2):
        """Merge two dictionaries or pydantic objects."""
        ob1 = dict(ob1)
        ob2 = dict(ob2)

        return {**ob1, **ob2}

    def __init__(self, manifest: DeploymentSchema, target_manifest: BaseResourceSchema):
        """Initialize the resource."""

        manifest.spec.targetResource.options = self.merge_dicts_or_pydantic(
            target_manifest.spec.options, manifest.spec.targetResource.options
        )

        self.target_manifest = target_manifest

        parent_labels = {
            "parent": f"{self.manifest.kind.lower()}.{self.manifest.namespace}.{self.manifest.metadata.name}"
        }

        # Add the parent label to the manifest
        manifest.metadata.labels = self.merge_dicts_or_pydantic(
            parent_labels, manifest.metadata.labels
        )

        flock_label = {"flock": "true"}

        # Add the flock label to the manifest
        manifest.metadata.labels = self.merge_dicts_or_pydantic(
            flock_label, manifest.metadata.labels
        )

        self.metadata = client.V1ObjectMeta(
            name=manifest.metadata.name,
            namespace=manifest.namespace,
            labels=manifest.metadata.labels,
        )

        self.namespace = manifest.namespace
        self.manifest = manifest
        self.rendered_manifest = None
