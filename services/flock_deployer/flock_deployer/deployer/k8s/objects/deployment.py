"""Kubernetes Deployment controller."""

from flock_schemas.base import BaseFlockSchema
from kubernetes import client

from flock_deployer.deployer.k8s.objects.base import K8sResource
from flock_deployer.deployer.k8s.objects.pod_template import FlockPodTemplateSpec
from flock_deployer.schemas.deployment import DeploymentSchema


class K8sDeployment(K8sResource):
    """Kubernetes Deployment object."""

    def __init__(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        super().__init__(manifest, target_manifest)
        self.rendered_manifest = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=self.metadata,
            spec=client.V1DeploymentSpec(
                replicas=manifest.spec.replicas,
                selector=client.V1LabelSelector(match_labels=manifest.metadata.labels),
                template=FlockPodTemplateSpec(
                    manifest, target_manifest
                ).pod_template_spec,
            ),
        )

    def create(self):
        """Create the deployment."""
        api_instance = client.AppsV1Api()
        api_instance.create_namespaced_deployment(
            body=self.rendered_manifest, namespace=self.namespace
        )
