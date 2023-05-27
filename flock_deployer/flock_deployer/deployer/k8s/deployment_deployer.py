"""Base class for a deployer"""

import time

from flock_schemas import BaseFlockSchema
from flock_schemas.deployment import DeploymentSchema
from flock_secrets_store import SecretStore
from kubernetes import client, config

from flock_deployer.deployer.base import BaseDeployer
from flock_deployer.deployer.k8s.common import set_dry_run
from flock_deployer.deployer.k8s.objects.deployment import K8sDeployment


class K8sDeploymentDeployer(BaseDeployer):
    """Abstract class for a deployer"""

    def __init__(self, secret_store: SecretStore = NotImplemented):
        """Initialize the deployer"""
        super().__init__(secret_store)
        config.load_kube_config()
        self.client = client.AppsV1Api()

    def _create_deployment_obj(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema
    ) -> K8sDeployment:
        """Create a Kubernetes Deployment object from the manifest"""
        deployment = K8sDeployment(manifest, target_manifest)

        return deployment

    def _patch_deployment(self, deployment: K8sDeployment, dry_run=None):
        """Patch a deployment in Kubernetes"""

        response = self.client.patch_namespaced_deployment(
            name=deployment.manifest.metadata.name,
            namespace=deployment.namespace,
            body=deployment.rendered_manifest,
            dry_run=dry_run,
        )

        print(f"Deployment updated. status='{response.status}'")

    def _delete(self, name, namespace, dry_run=None):
        """Delete a deployment in Kubernetes"""

        api_response = self.client.delete_namespaced_deployment(
            name=name,
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground",
                grace_period_seconds=0,
                dry_run=[dry_run] if dry_run else None,
            ),
            dry_run=dry_run,
        )
        print(f"Deployment deleted. status='{api_response.status}'")  # type: ignore

    def _create(self, deployment: K8sDeployment, dry_run=None):
        """Create a deployment in Kubernetes"""

        response = self.client.create_namespaced_deployment(
            body=deployment.rendered_manifest,
            namespace=deployment.namespace,
            dry_run=dry_run,
        )
        print(f"Deployment created. status='{response.status}'")  # type: ignore

    def _update(self, deployment: K8sDeployment, dry_run=None):
        """Update a deployment in Kubernetes"""

        try:
            self._patch_deployment(deployment, dry_run)
        except client.ApiException:
            self._delete(
                name=deployment.metadata.name,
                namespace=deployment.namespace,
                dry_run=dry_run,
            )
            while self.exists(
                name=deployment.manifest.metadata.name, namespace=deployment.namespace
            ):
                time.sleep(0.33)
            self._create(deployment, dry_run)

    def delete(self, name, namespace, dry_run=None):
        """Delete a deployment from Kubernetes"""

        dry_run = set_dry_run(dry_run)

        try:
            self._delete(name, namespace, dry_run)
        except client.ApiException as error:
            print(f"Failed to delete deployment: {error}")

    def update(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Update a deployment in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        deployment = self._create_deployment_obj(manifest, target_manifest)

        try:
            self._patch_deployment(deployment, dry_run)
        except client.ApiException:
            self._delete(manifest, dry_run)
            while self.exists(
                name=manifest.metadata.name, namespace=manifest.namespace
            ):
                time.sleep(0.33)
            self._create(deployment, dry_run)

    def deploy(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Deploy service and deployment to Kubernetes"""

        dry_run = set_dry_run(dry_run)

        deployment = self._create_deployment_obj(manifest, target_manifest)

        if self.exists(name=manifest.metadata.name, namespace=manifest.namespace):
            try:
                self._update(deployment, dry_run)
            except client.ApiException as error:
                print(f"Failed to update deployment: {error}")
        else:
            try:
                self._create(deployment, dry_run)
            except client.ApiException as error:
                print(f"Failed to create deployment: {error}")

    def exists(self, name: str, namespace: str):
        """Check if a deployment exists"""

        try:
            self.client.read_namespaced_deployment(name=name, namespace=namespace)
            return True
        except client.ApiException as error:
            if error.status == 404:
                return False
            raise

    def create(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Create a deployment in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        deployment = self._create_deployment_obj(manifest, target_manifest)

        try:
            self._create(deployment, dry_run)
        except client.ApiException as error:
            print(f"Failed to create deployment: {error}")
