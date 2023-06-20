"""Base class for a deployer"""

import logging
import os
import time

from kubernetes import client, config

from flock_deployer.deployer.base import BaseDeployer
from flock_deployer.deployer.k8s.common import set_dry_run
from flock_deployer.deployer.k8s.objects.service import K8sService
from flock_deployer.schemas.deployment import DeploymentSchema


class K8sServiceDeployer(BaseDeployer):
    """Abstract class for a deployer"""

    def __init__(
        self,
    ) -> None:
        """Initialize the deployer"""

        if os.environ.get("LOCAL", ""):
            config.load_kube_config()
            logging.debug("Using local kube config")
        else:
            config.load_incluster_config()
            logging.debug("Using in-cluster kube config")

        self.client = client.CoreV1Api()

    def _create_service_obj(self, manifest: DeploymentSchema) -> K8sService:
        """Create a Kubernetes Service object from the manifest"""

        service = K8sService(manifest)

        return service

    def _create(self, service: K8sService, dry_run=None):
        """Create a service in Kubernetes"""

        response = self.client.create_namespaced_service(
            body=service.rendered_manifest, namespace=service.namespace, dry_run=dry_run
        )
        logging.info(
            "Service %s created in %s", service.metadata.name, service.namespace
        )
        logging.info(response.status)  # type: ignore

    def _patch(self, service: K8sService, dry_run=None):
        """Patch a service in Kubernetes"""

        response = self.client.patch_namespaced_service(
            name=service.manifest.metadata.name,
            namespace=service.namespace,
            body=service.rendered_manifest,
            dry_run=dry_run,
        )
        logging.info(
            "Service %s updated in %s", service.metadata.name, service.namespace
        )
        logging.info(response.status)  # type: ignore

    def _delete(self, name, namespace, dry_run=None):
        """Delete a deployment in Kubernetes"""

        response = self.client.delete_namespaced_service(
            name=name,
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground",
                grace_period_seconds=0,
                dry_run=[dry_run] if dry_run else None,
            ),
            dry_run=dry_run,
        )
        logging.info("Service %s deleted in %s", name, namespace)
        logging.info(response.status)  # type: ignore

    def _update(self, service: K8sService, dry_run=None):
        """Update a service in Kubernetes"""

        try:
            self._patch(service, dry_run)
        except client.ApiException:
            self._delete(service, dry_run)
            while self.exists(
                name=service.manifest.metadata.name, namespace=service.namespace
            ):
                time.sleep(0.33)
            self._create(service, dry_run)

    def deploy(self, manifest: DeploymentSchema, _, dry_run=None):
        """Deploy service and deployment to Kubernetes"""

        dry_run = set_dry_run(dry_run)

        service_obj = self._create_service_obj(manifest)

        if self.exists(name=manifest.metadata.name, namespace=manifest.namespace):
            try:
                self._update(service_obj, dry_run)
            except client.ApiException as error:
                logging.error(
                    "Failed to update service %s in %s",
                    manifest.metadata.name,
                    manifest.namespace,
                )
                logging.error(error)
        else:
            try:
                self._create(service_obj, dry_run)
            except client.ApiException as error:
                logging.error(
                    "Failed to create service %s in %s",
                    manifest.metadata.name,
                    manifest.namespace,
                )
                logging.error(error)

    def delete(self, name: str, namespace: str, dry_run=None):
        """Delete a deployment from Kubernetes"""

        dry_run = set_dry_run(dry_run)

        try:
            self._delete(name, namespace, dry_run)
        except client.ApiException as error:
            print(f"Failed to delete service: {error}")

    def exists(self, name, namespace):
        """Check if a service exists"""

        try:
            self.client.read_namespaced_service(name=name, namespace=namespace)
            return True
        except client.ApiException as error:
            if error.status == 404:
                return False
            raise

    def update(self, manifest: DeploymentSchema, _, dry_run=None):
        """Update a service in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        service_obj = self._create_service_obj(manifest)

        try:
            self._patch(service_obj, dry_run)
        except client.ApiException:
            self._delete(service_obj, dry_run)
            while self.exists(
                name=manifest.metadata.name,
                namespace=manifest.namespace,
            ):
                time.sleep(0.33)
            self._create(service_obj, dry_run)

    def create(self, manifest: DeploymentSchema, _, dry_run=None):
        """Create a service in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        deployment = self._create_service_obj(manifest)

        try:
            self._create(deployment, dry_run)
        except client.ApiException as error:
            logging.error(
                "Failed to create service %s in %s",
                manifest.metadata.name,
                manifest.namespace,
            )
            logging.error(error)
