"""Kubernetes Job controller."""


from flock_schemas import BaseFlockSchema
from flock_schemas.job import CronJobSchema, JobSchema
from kubernetes import client

from flock_deployer.deployer.k8s.objects.base import K8sResource
from flock_deployer.deployer.k8s.objects.pod_template import FlockPodTemplateSpec


class K8sJob(K8sResource):
    """Kubernetes Job object."""

    def __init__(self, manifest: JobSchema, target_manifest: BaseFlockSchema):
        super().__init__(manifest, target_manifest)
        self.rendered_manifest = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=self.metadata,
            spec=client.V1JobSpec(
                template=FlockPodTemplateSpec(
                    manifest, target_manifest
                ).pod_template_spec,
                backoff_limit=manifest.spec.backoff_limit,
                completions=manifest.spec.completions,
                parallelism=manifest.spec.parallelism,
            ),
        )

    def create(self):
        """Create the job."""
        api_instance = client.BatchV1Api()
        api_instance.create_namespaced_job(
            body=self.rendered_manifest, namespace=self.namespace
        )


class K8sCronJob(K8sResource):
    """Kubernetes CronJob object."""

    def __init__(self, manifest: CronJobSchema, target_manifest: BaseFlockSchema):
        super().__init__(manifest, target_manifest)
        self.rendered_manifest = client.V1CronJob(
            api_version="batch/v1beta1",
            kind="CronJob",
            metadata=self.metadata,
            spec=client.V1CronJobSpec(
                schedule=manifest.spec.schedule,
                job_template=client.V1JobTemplateSpec(
                    spec=client.V1JobSpec(
                        template=FlockPodTemplateSpec(
                            manifest, target_manifest
                        ).pod_template_spec,
                        backoff_limit=manifest.spec.backoff_limit,
                        completions=manifest.spec.completions,
                        parallelism=manifest.spec.parallelism,
                    ),
                ),
            ),
        )

    def create(self):
        """Create the CronJob."""
        api_instance = client.BatchV1Api()
        api_instance.create_namespaced_cron_job(
            body=self.rendered_manifest, namespace=self.namespace
        )
