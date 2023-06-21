"""Kubernetes PodTemplateSpec object."""
from typing import Union

from flock_deployer.schemas.deployment import (  # VolumeEmptyDir,; VolumeHostPath,; VolumePersistentVolumeClaim,
    ContainerSpec,
    DeploymentSchema,
    EnvFrom,
    Volume,
)
from flock_deployer.schemas.job import CronJobSchema, JobSchema
from flock_schemas.base import BaseResourceSchema
from kubernetes import client


class FlockPodTemplate:
    """Kubernetes PodTemplateSpec object."""

    def __init__(
        self,
        manifest: Union[DeploymentSchema, JobSchema, CronJobSchema],
        target_manifest: BaseResourceSchema,
    ) -> None:
        container_spec = ContainerSpec(**manifest.spec.container.dict())
        self.pod_template_spec = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=manifest.metadata.labels),
            spec=client.V1PodSpec(
                restart_policy=manifest.spec.restart_policy,
                containers=[
                    client.V1Container(
                        args=container_spec.args,
                        image_pull_policy=container_spec.image_pull_policy,
                        name=manifest.metadata.name,
                        image=container_spec.image,
                        env=self._build_env(container_spec, target_manifest),
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

    def _build_env(
        self, container_spec: ContainerSpec, target_manifest: BaseResourceSchema
    ) -> list[client.V1EnvVar]:
        result = [
            client.V1EnvVar(
                name=env_item.name,
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=env_item.valueFrom.secretKeyRef.name,
                        key=env_item.valueFrom.secretKeyRef.key,
                    )
                ),
            )
            if isinstance(env_item, EnvFrom)
            else client.V1EnvVar(
                name=env_item.name,
                value=env_item.value,
            )
            for env_item in container_spec.env
        ]
        result += [
            client.V1EnvVar(
                name="FLOCK_SCHEMA_VALUE",
                value=target_manifest.json(),
            )
        ]
        return result

    def volume_source_to_k8s(self, volume: Volume):
        """Convert a volume source to a Kubernetes volume source."""

        return {
            "name": volume.name,
            "persistent_volume_claim": client.V1PersistentVolumeClaimVolumeSource(
                claim_name=volume.persistentVolumeClaim.claimName,
                read_only=volume.readOnly,
            ),
        }
