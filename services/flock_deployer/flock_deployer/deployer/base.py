"""Base class for a deployer"""


import abc
import logging
import random
import string
from typing import Callable, List, Union

from flock_common.secret_store import SecretStore
from flock_deployer.config_store import ConfigStore
from flock_deployer.schemas.config import DeploymentConfigSchema
from flock_deployer.schemas.deployment import (
    ContainerPort,
    ContainerSpec,
    DeploymentSchema,
    DeploymentSpec,
    EnvFrom,
    EnvVar,
    PersistentVolumeClaim,
    TargetResource,
    Volume,
    VolumeMount,
)
from flock_deployer.schemas.job import (
    BaseMetaData,
    CronJobSchema,
    CronJobSpec,
    JobSchema,
    JobSpec,
)
from flock_resource_store.base import ResourceStore
from flock_schemas.base import BaseResourceSchema
from flock_schemas.factory import SchemaFactory


class BaseDeployer(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    @abc.abstractmethod
    def deploy(self, manifest, target_manifest: BaseResourceSchema, dry_run=None):
        """Deploy"""

    def update(self, manifest, target_manifest: BaseResourceSchema, dry_run=None):
        """Update"""

    @abc.abstractmethod
    def create(self, manifest, target_manifest: BaseResourceSchema, dry_run=None):
        """Create"""

    @abc.abstractmethod
    def delete(self, name, namespace, dry_run=None):
        """Delete"""

    @abc.abstractmethod
    def exists(self, name, namespace):
        """Check if deployment exists"""


class BaseDeployers(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    def __init__(
        self,
        resource_store: ResourceStore,
        secret_store: SecretStore,
        config_store: ConfigStore,
    ) -> None:
        """Initialize the deployer"""
        self.secret_store: SecretStore = secret_store
        self.resource_store = resource_store
        self.config_store = config_store
        self.schema_factory = SchemaFactory()
        self.schema_creators_map = {
            "FlockDeployment": self.create_deployment_schema,
            "FlockJob": self.create_job_schema,
            "FlockCronJob": self.create_cronjob_schema,
        }

        self.service_deployer: BaseDeployer
        self.deployment_deployer: BaseDeployer
        self.cronjob_deployer: BaseDeployer
        self.job_deployer: BaseDeployer

    def _random_suffix(self, s, length):
        # Generate a random string of the given length
        suffix = "".join(random.choices(string.ascii_letters + string.digits, k=length))

        # Append the random string to the input string
        return f"{s}-{suffix}".lower()

    def get_creator(
        self, kind
    ) -> Callable[..., Union[DeploymentSchema, JobSchema, CronJobSchema]]:
        """
        Get the creator for a deployment or a job

        Args:
            kind (str): The kind of the deployment or job

        Raises:
            ValueError: If the creator is not found

        Returns:
            Callable[..., Union[DeploymentSchema, JobSchema]]: The creator
            expects the following keyword arguments:
                name (str): The name of the deployment or job
                namespace (str): The namespace of the deployment or job
                target_manifest (BaseResourceSchema): The target manifest
                config (DeploymentConfigSchema): The deployment config
        """

        creator = self.schema_creators_map.get(kind, None)
        if not creator:
            msg = f"Deployment Schema Creator not found for kind {kind}"
            logging.error(msg)
            raise ValueError(msg)
        return creator

    def get_target_manifest(self, name, namespace, kind) -> BaseResourceSchema:
        """Get the target manifest for a deployment"""

        schema_cls = self.schema_factory.get_schema(kind)
        target_manifest = self.resource_store.get(
            kind=kind, name=name, namespace=namespace
        )
        target_manifest = schema_cls(**target_manifest)
        return target_manifest

    def _get_target_resource(
        self, target_manifest: BaseResourceSchema
    ) -> TargetResource:
        return TargetResource(  # type: ignore
            kind=target_manifest.kind,
            name=target_manifest.metadata.name,
            namespace=target_manifest.namespace,
            description=target_manifest.metadata.description,
            options=target_manifest.spec.options,
            # TODO: i have no idea why description and options must be included here by pylance if it's optional in the schema
        )

    def _get_container_spec(
        self, target_manifest: BaseResourceSchema, config: DeploymentConfigSchema
    ) -> ContainerSpec:
        return ContainerSpec(
            volume_mounts=[
                VolumeMount(
                    name="flock-data",
                    mountPath="/flock-data",
                    readOnly=False,
                )
            ],
            # TODO: fetch image from global config
            image=self.fetch_image(target_manifest.kind),
            image_pull_policy="IfNotPresent",
            ports=[
                ContainerPort(
                    name="http",
                    port=8080,
                    protocol="TCP",
                )
            ],
            env=self.env_vars(target_manifest, config),
        )

    def _merge_config_with_global_defaults(
        self, config: DeploymentConfigSchema, target_kind: str
    ) -> DeploymentConfigSchema:
        """Merge the config with the default global config
        Give precedence to the config passed in
        """

        # Get names of environment variables from the passed-in config
        existing_env_names = {env.name for env in config.env}

        # Define a helper function to merge environment variables
        def merge_envs(source_config):
            if source_config:
                source_config = DeploymentConfigSchema(**source_config)
                # Only add env variables that are not already in the existing config
                config.env.extend(
                    env
                    for env in source_config.env
                    if env.name not in existing_env_names
                )

        # Merge global config
        global_config = self.config_store.get(name="global")
        merge_envs(global_config)

        # Merge kind-specific global config
        kind_global_config = self.config_store.get(name=f"{target_kind}_global".lower())
        merge_envs(kind_global_config)

        return config

    def create_deployment_schema(
        self,
        name,
        namespace,
        target_manifest: BaseResourceSchema,
        config: DeploymentConfigSchema,
        **kwargs,
    ) -> DeploymentSchema:
        """Create deployment manifest"""

        deployment_manifest = DeploymentSchema(
            apiVersion="flock/v1",
            kind="FlockDeployment",
            namespace=namespace,
            metadata=BaseMetaData(
                name=name,
                description=target_manifest.metadata.description,
                labels=target_manifest.metadata.labels,
            ),
            spec=DeploymentSpec(
                targetResource=self._get_target_resource(target_manifest),
                volumes=[
                    Volume(
                        name="flock-data",
                        readOnly=False,
                        persistentVolumeClaim=PersistentVolumeClaim(claimName="flock"),
                    )
                ],
                replicas=1,
                container=self._get_container_spec(target_manifest, config),
                restart_policy="Always",
            ),
        )

        return deployment_manifest

    def create_job_schema(
        self,
        name,
        namespace,
        target_manifest: BaseResourceSchema,
        config: DeploymentConfigSchema,
        **kwargs,
    ) -> JobSchema:
        """Create job manifest"""

        job_manifest = JobSchema(
            apiVersion="flock/v1",
            kind="FlockJob",
            namespace=namespace,
            metadata=BaseMetaData(
                name=self._random_suffix(name, 5),
                description=target_manifest.metadata.description,
                labels=target_manifest.metadata.labels,
            ),
            spec=JobSpec(
                targetResource=self._get_target_resource(target_manifest),
                container=self._get_container_spec(target_manifest, config),
                restart_policy="Never",
                volumes=[
                    Volume(
                        name="flock-data",
                        persistentVolumeClaim=PersistentVolumeClaim(claimName="flock"),
                        readOnly=False,
                    )
                ],
            ),
        )
        return job_manifest

    def create_cronjob_schema(
        self,
        name,
        namespace,
        target_manifest: BaseResourceSchema,
        config: DeploymentConfigSchema,
        **kwargs,
    ) -> JobSchema:
        """Create job manifest"""

        job_manifest = CronJobSchema(
            apiVersion="flock/v1",
            kind="FlockCronJob",
            namespace=namespace,
            metadata=BaseMetaData(
                name=self._random_suffix(name, 5),
                description=target_manifest.metadata.description,
                labels=target_manifest.metadata.labels,
            ),
            spec=CronJobSpec(
                schedule=kwargs["schedule"],
                targetResource=self._get_target_resource(target_manifest),
                container=self._get_container_spec(target_manifest, config),
                restart_policy="Never",
                volumes=[
                    Volume(
                        name="flock-data",
                        persistentVolumeClaim=PersistentVolumeClaim(claimName="flock"),
                        readOnly=False,
                    )
                ],
            ),
        )
        return job_manifest

    def fetch_image(self, target_kind: str):
        """Fetch image name dynamically based on target kind from system configuration"""
        # TODO: make it actually dynamic, from some global configuration

        if target_kind == "Agent":
            return "flock-agent:latest"
        if target_kind == "EmbeddingsLoader":
            return "flock-embeddings-loader:latest"
        if target_kind == "WebScraper":
            return "flock-webscraper:latest"

        raise NotImplementedError

    def env_vars(
        self, target_manifest: BaseResourceSchema, config: DeploymentConfigSchema
    ) -> List[Union[EnvVar, EnvFrom]]:
        """Fetch env vars dynamically"""
        target_kind = target_manifest.kind
        env_addition: List[Union[EnvVar, EnvFrom]] = []
        result: List[Union[EnvVar, EnvFrom]] = []

        # TODO: find a way to get rid of this hack
        if target_kind == "WebScraper":
            env_addition.append(
                EnvVar(
                    name="SCRAPER_NAME",
                    value=target_manifest.spec.dependencies[0].name,  # type: ignore
                )
            )
        result = config.env + env_addition
        result = self._merge_config_with_global_defaults(config, target_kind).env

        return result
