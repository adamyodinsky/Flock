"""Kubernetes Deployment controller."""

from flock_schemas import BaseFlockSchema
from flock_schemas.deployment import DeploymentSchema
from kubernetes import client

from flock_deployer.deployers.k8s.objects.base import K8sResource


class K8sDeployment(K8sResource):
    """Kubernetes Deployment object."""

    def __init__(self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema):
        super().__init__(manifest, target_manifest)
        self.rendered_manifest = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(
                name=manifest.metadata.name,
                namespace=manifest.namespace,
                labels=manifest.metadata.labels,
            ),
            spec=client.V1DeploymentSpec(
                replicas=manifest.spec.replicas,
                selector=client.V1LabelSelector(match_labels=manifest.metadata.labels),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels=manifest.metadata.labels),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                image_pull_policy=manifest.spec.container.image_pull_policy,
                                name=manifest.metadata.name,
                                image=manifest.spec.container.image,
                                env=[
                                    client.V1EnvVar(name=key, value=value)
                                    for key, value in self.manifest.spec.container.env.items()
                                ]
                                + [
                                    client.V1EnvVar(
                                        name="FLOCK_SCHEMA_VALUE",
                                        value=self.target_manifest.json(),
                                    )
                                ],
                                volume_mounts=[],
                                ports=[
                                    client.V1ContainerPort(
                                        name=port.name,
                                        protocol=port.protocol,
                                        host_port=port.host_port,
                                        container_port=port.container_port,
                                        host_ip=port.host_ip,
                                    )
                                    for port in self.manifest.spec.container.ports
                                ],
                            )
                        ],
                        volumes=[],
                    ),
                ),
            ),
        )

    def add_volume(self, volume: client.V1Volume):
        """Add a volume to the deployment."""
        self.rendered_manifest.spec.template.spec.volumes.append(volume)

    def add_volume_mount(self, volume_mount: client.V1VolumeMount):
        """Add a volume mount to the deployment."""
        self.rendered_manifest.spec.template.spec.containers[0].volume_mounts.append(
            volume_mount
        )

    def add_port(self, port: client.V1ContainerPort):
        """Add a port to the deployment."""
        self.rendered_manifest.spec.template.spec.containers[0].ports.append(port)

    def add_env(self, env: client.V1EnvVar):
        """Add an environment variable to the deployment."""
        self.rendered_manifest.spec.template.spec.containers[0].env.append(env)

    def create(self):
        """Create the deployment."""
        api_instance = client.AppsV1Api()
        api_instance.create_namespaced_deployment(
            body=self.rendered_manifest, namespace=self.namespace
        )
