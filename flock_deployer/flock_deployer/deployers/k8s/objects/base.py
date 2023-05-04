"""Kubernetes Deployment controller."""

import abc

from flock_schemas.deployment import DeploymentSchema


class K8sResource(metaclass=abc.ABCMeta):
    """Kubernetes Resource object."""

    def __init__(self, manifest: DeploymentSchema):
        """Initialize the resource."""
        self.namespace = manifest.namespace
        self.rendered_manifest = None
