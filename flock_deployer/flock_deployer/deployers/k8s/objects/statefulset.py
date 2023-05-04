"""Kubernetes StatefulSet controller."""

from flock_schemas.deployment import DeploymentSchema
from kubernetes import client

from flock_deployer.deployers.k8s.objects.k8sResource import K8sResource


class K8sStatefulSet(K8sResource):
    """Kubernetes StatefulSet object."""

    def __init__(self, manifest: DeploymentSchema):
        super().__init__(manifest)
        self.rendered_manifest = client.V1StatefulSet(
            api_version="apps/v1",
            kind="StatefulSet",
            metadata=client.V1ObjectMeta(
                name=manifest.metadata.name,
                namespace=manifest.namespace,
                labels=manifest.metadata.labels,
            ),
            spec=client.V1StatefulSetSpec(
                replicas=manifest.spec.replicas,
                selector=client.V1LabelSelector(match_labels=manifest.metadata.labels),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels=manifest.metadata.labels),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                image=manifest.spec.image,
                                env=[
                                    client.V1EnvVar(name=key, value=value)
                                    for key, value in manifest.spec.targetResource.env.items()
                                ],
                                volume_mounts=[],
                                ports=[client.V1ContainerPort(container_port=80)],
                            )
                        ],
                        volumes=[],
                    ),
                ),
                service_name=manifest.metadata.name,
            ),
        )

    def add_volume(self, volume: client.V1Volume):
        """Add a volume to the statefulset."""
        self.rendered_manifest.spec.template.spec.volumes.append(volume)

    def add_volume_mount(self, volume_mount: client.V1VolumeMount):
        """Add a volume mount to the statefulset."""
        self.rendered_manifest.spec.template.spec.containers[0].volume_mounts.append(
            volume_mount
        )

    def add_port(self, port: client.V1ContainerPort):
        """Add a port to the statefulset."""
        self.rendered_manifest.spec.template.spec.containers[0].ports.append(port)

    def add_env(self, env: client.V1EnvVar):
        """Add an environment variable to the statefulset."""
        self.rendered_manifest.spec.template.spec.containers[0].env.append(env)
