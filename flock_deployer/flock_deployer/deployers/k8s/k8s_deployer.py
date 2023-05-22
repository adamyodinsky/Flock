"""Base class for a deployer"""

import time

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

    def deploy(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Deploy service and deployment to Kubernetes"""

        if dry_run is not None:
            dry_run = "All"

        deployment = self._create_deployment_obj(manifest, target_manifest)
        service = self._create_service_obj(manifest)

        if self._deployment_exists(
            manifest,
        ):
            try:
                self.__update_deployment(deployment, dry_run)
            except client.ApiException as error:
                print(f"Failed to update deployment: {error}")
        else:
            try:
                self.__create_deployment(deployment, dry_run)
            except client.ApiException as error:
                print(f"Failed to create deployment: {error}")

        if self._service_exists(manifest):
            try:
                self.__update_service(service, dry_run)
            except client.ApiException as error:
                print(f"Failed to update service: {error}")
        else:
            try:
                self.__create_service(service, dry_run)
            except client.ApiException as error:
                print(f"Failed to create service: {error}")

    def delete(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Delete a deployment from Kubernetes"""

        if dry_run is not None:
            dry_run = "All"

        deployment = self._create_deployment_obj(manifest, target_manifest)
        service = self._create_service_obj(manifest)

        try:
            self.__delete_deployment(deployment, dry_run)
        except client.ApiException as error:
            print(f"Failed to delete deployment: {error}")

        try:
            self.__delete_service(service, dry_run)
        except client.ApiException as error:
            print(f"Failed to delete service: {error}")

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

    def _create_deployment_obj(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema
    ) -> K8sDeployment:
        """Create a Kubernetes Deployment object from the manifest"""
        deployment = K8sDeployment(manifest, target_manifest)

        return deployment

    def __create_deployment(self, deployment: K8sDeployment, dry_run=None):
        """Create a deployment in Kubernetes"""

        response = self.apps_v1.create_namespaced_deployment(
            body=deployment.rendered_manifest,
            namespace=deployment.namespace,
            dry_run=dry_run,
        )
        print(f"Deployment created. status='{response.status}'")  # type: ignore

    def __patch_deployment(self, deployment: K8sDeployment, dry_run=None):
        """Patch a deployment in Kubernetes"""

        response = self.apps_v1.patch_namespaced_deployment(
            name=deployment.manifest.metadata.name,
            namespace=deployment.namespace,
            body=deployment.rendered_manifest,
            dry_run=dry_run,
        )

        print(f"Deployment updated. status='{response.status}'")

    def __delete_deployment(self, deployment: K8sDeployment, dry_run=None):
        """Delete a deployment in Kubernetes"""

        api_response = self.apps_v1.delete_namespaced_deployment(
            name=deployment.manifest.metadata.name,
            namespace=deployment.namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground",
                grace_period_seconds=0,
                dry_run=[dry_run] if dry_run else None,
            ),
            dry_run=dry_run,
        )
        print(f"Deployment deleted. status='{api_response.status}'")  # type: ignore

    def __update_deployment(self, deployment: K8sDeployment, dry_run=None):
        """Update a deployment in Kubernetes"""

        try:
            self.__patch_deployment(deployment, dry_run)
        except client.ApiException:
            self.__delete_deployment(deployment, dry_run)
            while self._deployment_exists(deployment.manifest):
                time.sleep(0.33)
            self.__create_deployment(deployment, dry_run)

    def _create_service_obj(self, manifest: DeploymentSchema) -> K8sService:
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

    def __create_service(self, service: K8sService, dry_run=None):
        """Create a service in Kubernetes"""

        response = self.core_v1.create_namespaced_service(
            body=service.rendered_manifest, namespace=service.namespace, dry_run=dry_run
        )
        print(f"Service created. status='{response.status}'")  # type: ignore

    def __patch_service(self, service: K8sService, dry_run=None):
        """Patch a service in Kubernetes"""

        response = self.core_v1.patch_namespaced_service(
            name=service.manifest.metadata.name,
            namespace=service.namespace,
            body=service.rendered_manifest,
            dry_run=dry_run,
        )
        print(f"Service updated. status='{response.status}'")

    def __delete_service(self, service: K8sService, dry_run=None):
        """Delete a deployment in Kubernetes"""

        api_response = self.core_v1.delete_namespaced_service(
            name=service.manifest.metadata.name,
            namespace=service.namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground",
                grace_period_seconds=0,
                dry_run=[dry_run] if dry_run else None,
            ),
            dry_run=dry_run,
        )
        print(f"Service deleted. status='{api_response.status}'")  # type: ignore

    def __update_service(self, service: K8sService, dry_run=None):
        """Update a service in Kubernetes"""

        try:
            self.__patch_service(service, dry_run)
        except client.ApiException:
            self.__delete_service(service, dry_run)
            while self._service_exists(service.manifest):
                time.sleep(0.33)
            self.__create_service(service, dry_run)
