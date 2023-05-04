"""Base class for a deployer"""

from flock_schemas.deployment import DeploymentSchema
from kubernetes import client, config

from flock_deployer.deployers.base import BaseDeployer
from flock_deployer.deployers.k8s.objects import K8sResourceFactory
from flock_deployer.deployers.k8s.objects.deployment import K8sDeployment
from flock_deployer.deployers.k8s.objects.k8sResource import K8sResource


class K8sDeployer(BaseDeployer):
    """Abstract class for a deployer"""

    def __init__(self):
        """Initialize the deployer"""
        config.load_kube_config()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()

    def _create_resource_object(self, manifest: DeploymentSchema) -> K8sResource:
        """Create a Kubernetes Deployment object from the manifest"""
        deployment = K8sDeployment(manifest)

        return deployment

    def deploy(self, manifest: DeploymentSchema):
        """Deploy to Kubernetes"""

        resource: K8sResource = K8sResourceFactory.create(manifest)
        response = self.apps_v1.create_namespaced_deployment(
            body=resource.rendered_manifest, namespace=resource.namespace
        )
        print(f"Deployment created. status='{response.status}'")

    def stop(self, manifest: DeploymentSchema):
        """Stop a deployment"""

        response = self.apps_v1.delete_namespaced_deployment(
            name=manifest.metadata.name,
            namespace=manifest.namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground", grace_period_seconds=5
            ),
        )
        print(f"Deployment stopped. status='{response.status}'")

    def kill(self, manifest: DeploymentSchema):
        """Kill a deployment"""

        response = self.apps_v1.delete_namespaced_deployment(
            name=manifest.metadata.name,
            namespace=manifest.namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Background", grace_period_seconds=0
            ),
        )
        print(f"Deployment killed. status='{response.status}'")
