from flock_schemas.deployment import DeploymentSchema
from kubernetes import client

from flock_deployer.deployer.k8s.objects.base import K8sResource


class K8sService(K8sResource):
    """Kubernetes Service object."""

    def __init__(self, manifest: DeploymentSchema):
        super().__init__(manifest, NotImplemented)
        self.rendered_manifest = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=manifest.metadata.name,
                namespace=manifest.namespace,
                labels=manifest.metadata.labels,
            ),
            spec=client.V1ServiceSpec(
                selector=manifest.metadata.labels,
                ports=[
                    client.V1ServicePort(
                        name=port.name,
                        protocol=port.protocol,
                        port=port.port,
                        target_port=port.port,
                    )
                    for port in manifest.spec.container.ports
                ],
            ),
        )
