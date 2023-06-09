"""Kubernetes Deployment controller."""

import abc

from kubernetes import client

from flock_deployer.schemas.base import BaseFlockSchema


class K8sResource(metaclass=abc.ABCMeta):
    """Kubernetes Resource object."""

    def __init__(self, manifest, target_manifest: BaseFlockSchema):
        """Initialize the resource."""

        if target_manifest is not NotImplemented:
            manifest.spec.targetResource.options = {
                **target_manifest.spec.options,
                **manifest.spec.targetResource.options,
            }
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
