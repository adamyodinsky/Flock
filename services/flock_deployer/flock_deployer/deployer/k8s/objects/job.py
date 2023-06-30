"""Kubernetes Job controller."""


from flock_schemas.base import BaseResourceSchema
from kubernetes import client

from flock_deployer.deployer.k8s.objects.base import K8sResource
from flock_deployer.deployer.k8s.objects.pod_template import FlockPodTemplate
from flock_deployer.schemas.job import CronJobSchema, JobSchema


class K8sJob(K8sResource):
    """Kubernetes Job object."""

    def __init__(self, manifest: JobSchema, target_manifest: BaseResourceSchema):
        super().__init__(manifest, target_manifest)

        manifest.spec.targetResource.options = self.merge_dicts_or_pydantic(
            target_manifest.spec.options, manifest.spec.targetResource.options
        )
        job_spec = self.get_job_spec(manifest, target_manifest)
        job_spec.template.spec.restart_policy = manifest.spec.restart_policy
        self.rendered_manifest = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=self.metadata,
            spec=job_spec,
        )

    def create(self):
        """Create the job."""
        api_instance = client.BatchV1Api()
        api_instance.create_namespaced_job(
            body=self.rendered_manifest, namespace=self.namespace
        )

    def get_job_spec(
        self, manifest: JobSchema, target_manifest: BaseResourceSchema
    ) -> client.V1JobSpec:
        job_spec = client.V1JobSpec(
            template=FlockPodTemplate(manifest, target_manifest).pod_template_spec,
            backoff_limit=manifest.spec.backoff_limit,
            completions=manifest.spec.completions,
            parallelism=manifest.spec.parallelism,
        )
        return job_spec


class K8sCronJob(K8sJob):
    """Kubernetes CronJob object."""

    def __init__(self, manifest: CronJobSchema, target_manifest: BaseResourceSchema):
        super().__init__(manifest, target_manifest)

        manifest.spec.targetResource.options = self.merge_dicts_or_pydantic(
            target_manifest.spec.options, manifest.spec.targetResource.options
        )

        job_spec = self.get_job_spec(manifest, target_manifest)
        self.rendered_manifest = client.V1CronJob(
            api_version="batch/v1",
            kind="CronJob",
            metadata=self.metadata,
            spec=client.V1CronJobSpec(
                schedule=manifest.spec.schedule,
                job_template=client.V1JobTemplateSpec(
                    spec=job_spec,
                ),
            ),
        )

    def create(self):
        """Create the CronJob."""
        api_instance = client.BatchV1Api()
        api_instance.create_namespaced_cron_job(
            body=self.rendered_manifest, namespace=self.namespace
        )
