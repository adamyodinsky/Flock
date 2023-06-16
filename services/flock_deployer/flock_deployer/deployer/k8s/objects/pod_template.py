"""Kubernetes PodTemplateSpec object."""
from flock_schemas.base import BaseFlockSchema
from kubernetes import client

from flock_deployer.schemas.deployment import (  # VolumeEmptyDir,; VolumeHostPath,; VolumePersistentVolumeClaim,
    ContainerSpec,
    Volume,
)


class FlockPodTemplate:
    """Kubernetes PodTemplateSpec object."""

    def __init__(self, manifest, target_manifest: BaseFlockSchema) -> None:
        container_spec = ContainerSpec(**manifest.spec.container.dict())
        self.pod_template_spec = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=manifest.metadata.labels),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        args=container_spec.args,
                        image_pull_policy=container_spec.image_pull_policy,
                        name=manifest.metadata.name,
                        image=container_spec.image,
                        env=[
                            client.V1EnvVar(
                                name=env_item.name,
                                value_from=client.V1EnvVarSource(
                                    secret_key_ref=client.V1SecretKeySelector(
                                        name=env_item.valueFrom["secretKeyRef"]["name"],
                                        key=env_item.valueFrom["secretKeyRef"]["key"],
                                    )
                                ),
                            )
                            if env_item.valueFrom
                            else client.V1EnvVar(
                                name=env_item.name,
                                value=env_item.value,
                            )
                            for env_item in container_spec.env
                        ]
                        + [
                            client.V1EnvVar(
                                name="FLOCK_SCHEMA_VALUE",
                                value=target_manifest.json(),
                            )
                        ],
                        volume_mounts=[
                            client.V1VolumeMount(
                                name=vol_mount.name,
                                mount_path=vol_mount.mountPath,
                                read_only=vol_mount.readOnly,
                            )
                            for vol_mount in container_spec.volume_mounts
                        ],
                        ports=[
                            client.V1ContainerPort(
                                name=port.name,
                                protocol=port.protocol,
                                container_port=port.port,
                            )
                            for port in container_spec.ports
                        ],
                    )
                ],
                volumes=[
                    client.V1Volume(**self.volume_source_to_k8s(vol))
                    for vol in manifest.spec.volumes
                ],
            ),
        )

    def volume_source_to_k8s(self, volume: Volume):
        """Convert a volume source to a Kubernetes volume source."""

        # source = volume.volume_source.__root__
        # if isinstance(source, VolumeEmptyDir):
        #     return {
        #         "name": volume.name,
        #         "empty_dir": client.V1EmptyDirVolumeSource(
        #             medium=source.medium,
        #             size_limit=source.sizeLimit,
        #         ),
        #     }
        # elif isinstance(source, VolumeHostPath):
        #     return {
        #         "name": volume.name,
        #         "host_path": client.V1HostPathVolumeSource(
        #             path=source.path,
        #             type=source.type,
        #         ),
        #     }
        # elif isinstance(source, VolumePersistentVolumeClaim):
        return {
            "name": volume.name,
            "persistent_volume_claim": client.V1PersistentVolumeClaimVolumeSource(
                claim_name=volume.persistentVolumeClaim.claimName,
                read_only=volume.readOnly,
            ),
        }
        # else:
        #     raise ValueError(f"Unsupported volume source type: {type(source).__name__}")
