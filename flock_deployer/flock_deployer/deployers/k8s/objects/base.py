"""Kubernetes Deployment controller."""

import abc

from flock_schemas import BaseFlockSchema, SchemasFactory
from flock_schemas.deployment import DeploymentSchema


class K8sResource(metaclass=abc.ABCMeta):
    """Kubernetes Resource object."""

    def __init__(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        """Initialize the resource."""

        if target_manifest is not NotImplemented:
            manifest.spec.targetResource.options = {
                **target_manifest.spec.options,  # type: ignore
                **manifest.spec.targetResource.options,  # type: ignore
            }
            self.target_manifest = SchemasFactory.get_schema(
                target_manifest.kind
            ).validate(target_manifest)
        else:
            self.target_manifest = None

        self.namespace = manifest.namespace
        self.manifest = manifest
        self.rendered_manifest = None
