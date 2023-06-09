"""Package for k8s resource objects."""

from flock_schemas import BaseFlockSchema
from flock_schemas.deployment import DeploymentSchema

from flock_deployer.deployer.k8s.objects.base import K8sResource
from flock_deployer.deployer.k8s.objects.deployment import K8sDeployment
from flock_deployer.deployer.k8s.objects.statefulset import K8sStatefulSet


class K8sResourceFactory:
    """Factory class for creating k8s resources."""

    @staticmethod
    def create(
        manifest: DeploymentSchema, target_manifest: BaseFlockSchema
    ) -> K8sResource:
        """Create a k8s resource."""
        if manifest.category == "deployment":
            return K8sDeployment(manifest, target_manifest)
        elif manifest.category == "statefulset":
            return K8sStatefulSet(manifest)
        else:
            raise ValueError(f"Unsupported resource type: {manifest.category}")
