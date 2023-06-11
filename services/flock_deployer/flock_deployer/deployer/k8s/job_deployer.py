"""Module for deploying Jobs to Kubernetes"""

from flock_common.secret_store import SecretStore
from flock_schemas.base import BaseFlockSchema
from kubernetes import client, config

from flock_deployer.deployer.base import BaseDeployer
from flock_deployer.deployer.k8s.common import set_dry_run
from flock_deployer.deployer.k8s.objects.job import K8sJob
from flock_deployer.schemas.job import JobSchema


class K8sJobDeployer(BaseDeployer):
    """Class for deploying Jobs"""

    def __init__(self, secret_store: SecretStore = NotImplemented):
        """Initialize the deployer"""
        super().__init__(secret_store)
        config.load_kube_config()
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
        print(f"Job deleted. status='{api_response.status}'")  # type: ignore

    def _create(self, job: K8sJob, dry_run=None):
        """Create a Job in Kubernetes"""

        response = self.client.create_namespaced_job(
            body=job.rendered_manifest,
            namespace=job.namespace,
            dry_run=dry_run,
        )
        print(f"Job created. status='{response.status}'")  # type: ignore

    def delete(self, name, namespace, dry_run=None):
        """Delete a Job from Kubernetes"""

        dry_run = set_dry_run(dry_run)

        try:
            self._delete(name, namespace, dry_run)
        except client.ApiException as error:
            print(f"Failed to delete Job: {error}")

    def deploy(
        self, manifest: JobSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Deploy a Job to Kubernetes"""

        dry_run = set_dry_run(dry_run)

        job = self._create_job_obj(manifest, target_manifest)

        try:
            self._create(job, dry_run)
        except client.ApiException as error:
            print(f"Failed to create Job: {error}")

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
            print(f"Failed to create Job: {error}")
