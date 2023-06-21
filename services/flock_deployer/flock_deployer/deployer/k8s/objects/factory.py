from flock_deployer.deployer.k8s.objects.base import K8sResource
from flock_deployer.deployer.k8s.objects.deployment import K8sDeployment
from flock_deployer.deployer.k8s.objects.job import K8sCronJob, K8sJob
from flock_schemas.base import BaseResourceSchema


class K8sResourceFactory:
    """Factory class for creating k8s resources."""

    @staticmethod
    def create(manifest, target_manifest: BaseResourceSchema) -> K8sResource:
        """Create a k8s resource."""
        if manifest.category == "deployment":
            return K8sDeployment(manifest, target_manifest)
        elif manifest.category == "job":
            return K8sJob(manifest, target_manifest)
        elif manifest.category == "cronjob":
            return K8sCronJob(manifest, target_manifest)
        else:
            raise ValueError(f"Unsupported resource type: {manifest.category}")
