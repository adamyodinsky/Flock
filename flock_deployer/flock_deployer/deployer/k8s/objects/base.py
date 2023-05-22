"""Kubernetes Deployment controller."""

import abc

from flock_schemas import BaseFlockSchema, SchemasFactory
from kubernetes import client


class K8sResource(metaclass=abc.ABCMeta):
    """Kubernetes Resource object."""

    def __init__(self, manifest, target_manifest: BaseFlockSchema):
        """Initialize the resource."""

        if target_manifest is not NotImplemented:
            manifest.spec.targetResource.options = {
                **target_manifest.spec.options,
                **manifest.spec.targetResource.options,
            }
            self.target_manifest = SchemasFactory.get_schema(
                target_manifest.kind
            ).validate(target_manifest)
        else:
            self.target_manifest = None

        self.metadata = (
            client.V1ObjectMeta(
                name=manifest.metadata.name,
                namespace=manifest.namespace,
                labels=manifest.metadata.labels,
            ),
        )
        self.namespace = manifest.namespace
        self.manifest = manifest
        self.rendered_manifest = None
