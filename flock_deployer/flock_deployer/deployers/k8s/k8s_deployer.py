"""Base class for a deployer"""

from flock_schemas import BaseFlockSchema
from flock_schemas.deployment import DeploymentSchema
from kubernetes import client, config

from flock_deployer.deployers.base import BaseDeployer
from flock_deployer.deployers.k8s.objects import K8sResourceFactory
from flock_deployer.deployers.k8s.objects.base import K8sResource
from flock_deployer.deployers.k8s.objects.deployment import K8sDeployment


class K8sDeployer(BaseDeployer):
    """Abstract class for a deployer"""

    def __init__(self):
        """Initialize the deployer"""
        config.load_kube_config()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()

    def _create_resource_object(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema
    ) -> K8sResource:
        """Create a Kubernetes Deployment object from the manifest"""
        deployment = K8sDeployment(manifest, target_manifest)

        return deployment

    def _create(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        """Deploy to Kubernetes"""

        resource: K8sResource = K8sResourceFactory.create(manifest, target_manifest)
        response = self.apps_v1.create_namespaced_deployment(
            body=resource.rendered_manifest, namespace=resource.namespace
        )
        print(f"Deployment created. status='{response.status}'")

    def _patch(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        """Deploy to Kubernetes"""

        resource: K8sResource = K8sResourceFactory.create(manifest, target_manifest)
        response = self.apps_v1.patch_namespaced_deployment(
            name=manifest.metadata.name,
            namespace=resource.namespace,
            body=resource.rendered_manifest,
        )
        print(f"Deployment created. status='{response.status}'")

    def _deployment_exists(self, manifest: DeploymentSchema):
        """Check if a deployment exists"""

        try:
            self.apps_v1.read_namespaced_deployment(
                name=manifest.metadata.name, namespace=manifest.namespace
            )
            return True
        except client.ApiException as error:
            if error.status == 404:
                return False
            else:
                raise

    def deploy(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        if self._deployment_exists(manifest):
            try:
                self._patch(manifest, target_manifest)
            except client.ApiException as error:
                print(f"Failed to update deployment: {error}")
        else:
            try:
                self._create(manifest, target_manifest)
            except client.ApiException as error:
                print(f"Failed to create deployment: {error}")

    # def stop(self, manifest: DeploymentSchema):
    #     """Stop a deployment"""

    #     response = self.apps_v1.delete_namespaced_deployment(
    #         name=manifest.metadata.name,
    #         namespace=manifest.namespace,
    #         body=client.V1DeleteOptions(
    #             propagation_policy="Foreground", grace_period_seconds=5
    #         ),
    #     )
    #     print(f"Deployment stopped. status='{response.status}'")

    # def kill(self, manifest: DeploymentSchema):
    #     """Kill a deployment"""

    #     response = self.apps_v1.delete_namespaced_deployment(
    #         name=manifest.metadata.name,
    #         namespace=manifest.namespace,
    #         body=client.V1DeleteOptions(
    #             propagation_policy="Background", grace_period_seconds=0
    #         ),
    #     )
    #     print(f"Deployment killed. status='{response.status}'")
