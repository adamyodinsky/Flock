"""Module for deploying CronJobs to Kubernetes"""


import logging

from flock_schemas.base import BaseFlockSchema
from kubernetes import client, config

from flock_deployer.deployer.base import BaseDeployer
from flock_deployer.deployer.k8s.common import set_dry_run
from flock_deployer.deployer.k8s.objects.job import K8sCronJob
from flock_deployer.schemas.job import CronJobSchema


class K8sCronJobDeployer(BaseDeployer):
    """Class for deploying CronJobs"""

    def __init__(self):
        """Initialize the deployer"""

        logging.debug("Initializing K8sCronJobDeployer")
        config.load_kube_config()
        self.client = client.BatchV1Api()

    def _create_cronjob_obj(
        self, manifest: CronJobSchema, target_manifest: BaseFlockSchema
    ) -> K8sCronJob:
        """Create a Kubernetes CronJob object from the manifest"""
        logging.debug(
            "Creating K8sCronJob object %s for namespace %s",
            manifest.metadata.name,
            manifest.namespace,
        )
        cronjob = K8sCronJob(manifest, target_manifest)

        return cronjob

    def _delete(self, name, namespace, dry_run=None):
        """Delete a CronJob in Kubernetes"""

        logging.debug("Deleting CronJob %s in namespace %s", name, namespace)
        try:
            response = self.client.delete_namespaced_cron_job(
                name=name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground",
                    grace_period_seconds=0,
                    dry_run=[dry_run] if dry_run else None,
                ),
                dry_run=dry_run,
            )
            logging.info("CronJob deleted")
            logging.info(response.status)  # type: ignore
        except client.ApiException as error:
            if error.status == 404:
                logging.info("CronJob %s not found, skipping", name)
            else:
                raise error

    def _update(self, cronjob: K8sCronJob, dry_run=None):
        """Update a CronJob in Kubernetes"""

        logging.debug(
            "Updating CronJob %s in namespace %s",
            cronjob.manifest.metadata.name,
            cronjob.namespace,
        )
        response = self.client.patch_namespaced_cron_job(
            name=cronjob.manifest.metadata.name,
            namespace=cronjob.namespace,
            body=cronjob.rendered_manifest,
            dry_run=dry_run,
        )

        logging.info("CronJob updated")
        logging.info(response.status)

    def _create(self, cronjob: K8sCronJob, dry_run=None):
        """Create a CronJob in Kubernetes"""

        logging.debug(
            "Creating CronJob %s in namespace %s",
            cronjob.manifest.metadata.name,
            cronjob.namespace,
        )

        response = self.client.create_namespaced_cron_job(
            body=cronjob.rendered_manifest,
            namespace=cronjob.namespace,
            dry_run=dry_run,
        )

        logging.info("CronJob created")
        logging.info(response.status)  # type: ignore

    def delete(self, name, namespace, dry_run=None):
        """Delete a CronJob from Kubernetes"""

        dry_run = set_dry_run(dry_run)
        logging.debug("Deleting CronJob %s in namespace %s", name, namespace)
        try:
            self._delete(name, namespace, dry_run)
        except client.ApiException as error:
            logging.error("Failed to delete CronJob: %s %s", name, namespace)
            logging.error(error)
            raise error

    def deploy(
        self, manifest: CronJobSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Deploy a CronJob to Kubernetes"""

        logging.info(
            "Deploying CronJob %s in namespace %s",
            manifest.metadata.name,
            manifest.namespace,
        )

        dry_run = set_dry_run(dry_run)

        cronjob = self._create_cronjob_obj(manifest, target_manifest)

        if self.exists(name=manifest.metadata.name, namespace=manifest.namespace):
            try:
                self._update(cronjob, dry_run)
            except client.ApiException as error:
                logging.error("Failed to update CronJob: %s", error)
                raise error
        else:
            try:
                self._create(cronjob, dry_run)
            except client.ApiException as error:
                logging.error(
                    "Failed to create CronJob: %s %s",
                    manifest.metadata.name,
                    manifest.namespace,
                )
                logging.error(error)
                raise error

    def exists(self, name: str, namespace: str):
        """Check if a CronJob exists"""

        try:
            self.client.read_namespaced_cron_job(name=name, namespace=namespace)
            logging.info("CronJob %s exists in namespace %s", name, namespace)
            return True
        except client.ApiException as error:
            if error.status == 404:
                return False
            raise error

    def create(
        self, manifest: CronJobSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Create a CronJob in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        cronjob = self._create_cronjob_obj(manifest, target_manifest)

        try:
            self._create(cronjob, dry_run)
        except client.ApiException as error:
            logging.error(
                "Failed to create CronJob: %s %s",
                manifest.metadata.name,
                manifest.namespace,
            )
            logging.error(error)
            raise error

    def update(
        self, manifest: CronJobSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Update a CronJob in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        cronjob = self._create_cronjob_obj(manifest, target_manifest)

        try:
            self._update(cronjob, dry_run)
        except client.ApiException as error:
            logging.error(
                "Failed to update CronJob: %s %s",
                manifest.metadata.name,
                manifest.namespace,
            )
            logging.error(error)
            raise error
