"""Module for deploying Jobs to Kubernetes"""


import logging
import os

from flock_schemas.base import BaseFlockSchema
from kubernetes import client, config

from flock_deployer.deployer.base import BaseDeployer
from flock_deployer.deployer.k8s.common import set_dry_run
from flock_deployer.deployer.k8s.objects.job import K8sJob
from flock_deployer.schemas.job import JobSchema


class K8sJobDeployer(BaseDeployer):
    """Class for deploying Jobs"""

    def __init__(self):
        """Initialize the deployer"""

        if os.environ.get("LOCAL", ""):
            config.load_kube_config()
            logging.debug("Using local kube config")
        else:
            config.load_incluster_config()
            logging.debug("Using in-cluster kube config")

        self.client = client.BatchV1Api()

    def _create_job_obj(
        self, manifest: JobSchema, target_manifest: BaseFlockSchema
    ) -> K8sJob:
        """Create a Kubernetes Job object from the manifest"""
        job = K8sJob(manifest, target_manifest)

        return job

    # TODO: delete does not work on jobs, have a bug in the code https://github.com/kubernetes-client/python/issues/1350
    def _delete(self, name, namespace, dry_run=None):
        """Delete a Job in Kubernetes"""

        try:
            api_response = self.client.delete_namespaced_job(
                name=name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground",
                    grace_period_seconds=0,
                    dry_run=[dry_run] if dry_run else None,
                ),
                dry_run=dry_run,
            )
            logging.info("Job deleted")
            logging.info(api_response.status)  # type: ignore
        except client.ApiException as error:
            if error.status == 404:
                logging.info("Job %s not found, skipping", name)
            else:
                raise error

    def _create(self, job: K8sJob, dry_run=None):
        """Create a Job in Kubernetes"""

        response = self.client.create_namespaced_job(
            body=job.rendered_manifest,
            namespace=job.namespace,
            dry_run=dry_run,
        )
        logging.info("Job created")
        logging.info(response.status)  # type: ignore

    def delete(self, name, namespace, dry_run=None):
        """Delete a Job from Kubernetes"""

        dry_run = set_dry_run(dry_run)

        try:
            self._delete(name, namespace, dry_run)
        except client.ApiException as error:
            logging.error("Failed to delete Job: %s", error)
            raise error

    def deploy(
        self, manifest: JobSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Deploy a Job to Kubernetes"""

        dry_run = set_dry_run(dry_run)

        job = self._create_job_obj(manifest, target_manifest)

        try:
            self._create(job, dry_run)
        except client.ApiException as error:
            logging.error("Failed to create Job: %s", error)

    def exists(self, name: str, namespace: str):
        """Check if a Job exists"""

        try:
            self.client.read_namespaced_job(name=name, namespace=namespace)
            return True
        except client.ApiException as error:
            if error.status == 404:
                return False
            raise

    def create(
        self, manifest: JobSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Create a Job in Kubernetes"""

        dry_run = set_dry_run(dry_run)

        job = self._create_job_obj(manifest, target_manifest)

        try:
            self._create(job, dry_run)
        except client.ApiException as error:
            logging.error("Failed to create Job: %s", error)
