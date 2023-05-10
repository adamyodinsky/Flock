"""Base class for a deployer"""

from flock_schemas import BaseFlockSchema
from flock_schemas.deployment import DeploymentSchema
from flock_secrets_store import SecretStore
from kubernetes import client, config

from flock_deployer.deployers.base import BaseDeployer
from flock_deployer.deployers.k8s.objects.deployment import K8sDeployment
from flock_deployer.deployers.k8s.objects.service import K8sService


class K8sDeployer(BaseDeployer):
    """Abstract class for a deployer"""

    def __init__(self, secret_store: SecretStore = NotImplemented):
        """Initialize the deployer"""
        super().__init__(secret_store)
        config.load_kube_config()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()

    def _create_deployment(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema
    ) -> K8sDeployment:
        """Create a Kubernetes Deployment object from the manifest"""
        deployment = K8sDeployment(manifest, target_manifest)

        return deployment

    def _create_service(self, manifest: DeploymentSchema) -> K8sService:
        """Create a Kubernetes Service object from the manifest"""
        service = K8sService(manifest)

        return service

    def _service_exists(self, manifest: DeploymentSchema):
        """Check if a service exists"""

        try:
            self.core_v1.read_namespaced_service(
                name=manifest.metadata.name, namespace=manifest.namespace
            )
            return True
        except client.ApiException as error:
            if error.status == 404:
                return False
            else:
                raise

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

    def dry_deploy(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        """Dry run of deployment to Kubernetes"""

        deployment = self._create_deployment(manifest, target_manifest)
        service = self._create_service(manifest)

        print(deployment.rendered_manifest)
        print(service.rendered_manifest)

    def deploy(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        """Deploy service and deployment to Kubernetes"""

        deployment = self._create_deployment(manifest, target_manifest)
        service = self._create_service(manifest)

        if self._deployment_exists(manifest):
            try:
                self.__patch_deployment(deployment)
            except client.ApiException as error:
                print(f"Failed to update deployment: {error}")
        else:
            try:
                self.__create_deployment(deployment)
            except client.ApiException as error:
                print(f"Failed to create deployment: {error}")

        if self._service_exists(manifest):
            try:
                self.__patch_service(service)
            except client.ApiException as error:
                print(f"Failed to update service: {error}")
        else:
            try:
                self.__create_service(service)
            except client.ApiException as error:
                print(f"Failed to create service: {error}")

    def __create_deployment(self, deployment: K8sDeployment):
        """Create a deployment in Kubernetes"""

        response = self.apps_v1.create_namespaced_deployment(
            body=deployment.rendered_manifest, namespace=deployment.namespace
        )
        print(f"Deployment created. status='{response.status}'")

    def __patch_deployment(self, deployment: K8sDeployment):
        """Patch a deployment in Kubernetes"""

        response = self.apps_v1.patch_namespaced_deployment(
            name=deployment.manifest.metadata.name,
            namespace=deployment.namespace,
            body=deployment.rendered_manifest,
        )
        print(f"Deployment updated. status='{response.status}'")

    def __create_service(self, service: K8sService):
        """Create a service in Kubernetes"""

        response = self.core_v1.create_namespaced_service(
            body=service.rendered_manifest, namespace=service.namespace
        )
        print(f"Service created. status='{response.status}'")

    def __patch_service(self, service: K8sService):
        """Patch a service in Kubernetes"""

        response = self.core_v1.patch_namespaced_service(
            name=service.manifest.metadata.name,
            namespace=service.namespace,
            body=service.rendered_manifest,
        )
        print(f"Service updated. status='{response.status}'")
