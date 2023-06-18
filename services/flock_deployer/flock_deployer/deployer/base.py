"""Base class for a deployer"""


import abc
import logging
import random
import string
from typing import List

from flock_common.secret_store import SecretStore
from flock_resource_store.base import ResourceStore
from flock_schemas.base import BaseFlockSchema
from flock_schemas.factory import SchemaFactory

from flock_deployer.config_store import ConfigStore, ConfigStoreFactory
from flock_deployer.schemas.
from flock_deployer.schemas.deployment import (
    ContainerPort,
    ContainerSpec,
    DeploymentSchema,
    DeploymentSpec,
    EnvironmentVariable,
    PersistentVolumeClaim,
    TargetResource,
    Volume,
    VolumeMount,
)
from flock_deployer.schemas.job import BaseMetaData, JobSchema, JobSpec


class BaseDeployer(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    @abc.abstractmethod
    def deploy(self, manifest, target_manifest: BaseFlockSchema, dry_run=None):
        """Deploy"""

    def update(self, manifest, target_manifest: BaseFlockSchema, dry_run=None):
        """Update"""

    @abc.abstractmethod
    def create(self, manifest, target_manifest: BaseFlockSchema, dry_run=None):
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
    ) -> None:
        """Initialize the deployer"""
        self.secret_store: SecretStore = secret_store
        self.resource_store = resource_store
        self.schema_factory = SchemaFactory()
        self.schema_creators_map = {
            "FlockDeployment": self.create_deployment_schema,
            "FlockJob": self.create_job_schema,
        }

        self.service_deployer: BaseDeployer
        self.deployment_deployer: BaseDeployer
        self.cron_job_deployer: BaseDeployer
        self.job_deployer: BaseDeployer

    def _random_suffix(self, s, length):
        # Generate a random string of the given length
        suffix = "".join(random.choices(string.ascii_letters + string.digits, k=length))

        # Append the random string to the input string
        return f"{s}-{suffix}".lower()

    def get_creator(self, kind):
        """Get the creator for a kind"""

        creator = self.schema_creators_map.get(kind, None)
        if not creator:
            msg = f"Deployment Schema Creator not found for kind {kind}"
            logging.error(msg)
            raise ValueError(msg)
        return creator

    def get_target_manifest(self, name, namespace, kind) -> BaseFlockSchema:
        """Get the target manifest for a deployment"""

        schema_cls = self.schema_factory.get_schema(kind)
        target_manifest = self.resource_store.get(
            kind=kind, name=name, namespace=namespace
        )
        target_manifest = schema_cls(**target_manifest)
        return target_manifest

    def _get_target_resource(self, target_manifest: BaseFlockSchema) -> TargetResource:
        return TargetResource(  # type: ignore
            kind=target_manifest.kind,
            name=target_manifest.metadata.name,
            namespace=target_manifest.namespace,
            # description=target_manifest.metadata.description,
            # options=target_manifest.spec.options,
            # TODO: i have no idea why description and options must be included here by pylance if it's optional in the schema
        )

    def _get_container_spec(self, target_manifest) -> ContainerSpec:
        return ContainerSpec(
            volume_mounts=[
                VolumeMount(
                    name="flock-data",
                    mountPath="/flock-data",
                    readOnly=False,
                )
            ],
            image=self.fetch_image(target_manifest.kind),
            image_pull_policy="IfNotPresent",
            ports=[
                ContainerPort(
                    name="http",
                    port=8080,
                    protocol="TCP",
                )
            ],
            env=self.fetch_env_vars(target_manifest),
        )

    def create_deployment_schema(
        self, name, namespace, target_manifest: BaseFlockSchema
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
                container=self._get_container_spec(target_manifest),
            ),
        )

        return deployment_manifest

    def create_job_schema(
        self, name, namespace, target_manifest: BaseFlockSchema
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
                container=self._get_container_spec(target_manifest),
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

    def fetch_env_vars(
        self, target_manifest: BaseFlockSchema
    ) -> List[EnvironmentVariable]:
        """Fetch env vars dynamically"""
        target_kind = target_manifest.kind
        result = []

        if target_kind == "Agent":
            result = self.get_vars(target_manifest)
        if target_kind == "EmbeddingsLoader":
            result = self.get_vars(target_manifest)
        if target_kind == "WebScraper":
            env_addition = EnvironmentVariable(  # type: ignore
                name="SCRAPER_NAME",
                value=target_manifest.spec.dependencies[0].name,
            )
            result = self.get_vars(target_manifest) + [env_addition]

        return result

    def get_vars(self, target_manifest: BaseFlockSchema) -> List[EnvironmentVariable]:
        return [
            EnvironmentVariable(  # type: ignore
                name="RESOURCE_STORE_HOST",
                value="flock-resource-store",
            ),
            EnvironmentVariable(  # type: ignore
                name="RESOURCE_STORE_USERNAME",
                value="root",
            ),
            EnvironmentVariable(  # type: ignore
                name="RESOURCE_STORE_PASSWORD",
                value="password",
            ),
            EnvironmentVariable(  # type: ignore
                name="QUEUE_HOST",
                value="flock-queue-rabbitmq-headless",
            ),
            EnvironmentVariable(  # type: ignore
                name="MANAGEMENT_STORE_HOST",
                value="flock-resource-store",
            ),
            EnvironmentVariable(  # type: ignore
                name="FLOCK_AGENT_HOST",
                value="0.0.0.0",
            ),
            EnvironmentVariable(  # type: ignore
                name="FLOCK_AGENT_PORT",
                value="8080",
            ),
            EnvironmentVariable(  # type: ignore
                name="SOURCE_DIR",
                value="/flock-data/embeddings/pre_processed",
            ),
            EnvironmentVariable(  # type: ignore
                name="SCRAPER_OUTPUT_DIR",
                value="/flock-data/embeddings/pre_processed",
            ),
            EnvironmentVariable(  # type: ignore
                name="ARCHIVE_DIR",
                value="/flock-data/embeddings/processed",
            ),
            EnvironmentVariable(  # type: ignore
                name="OPENAI_API_KEY",
                valueFrom={
                    "secretKeyRef": {
                        "name": "mysecret",
                        "key": "openai-token",
                    }
                },
            ),
            EnvironmentVariable(  # type: ignore
                name="SERPAPI_API_KEY",
                valueFrom={
                    "secretKeyRef": {
                        "name": "mysecret",
                        "key": "serpapi-token",
                    }
                },
            ),
            EnvironmentVariable(  # type: ignore
                name="FLOCK_LOADER_TYPE",
                value="scraped-data",
            ),
        ]
