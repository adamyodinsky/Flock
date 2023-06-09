"""Manifest creator. creation of full flock deployments/job/cronjob manifests from small amount of data input"""
from typing import List

from flock_deployer.manifest_creator.base import BaseManifestCreator
from flock_deployer.schemas.base import BaseFlockSchema
from flock_deployer.schemas.deployment import (
    ContainerPort,
    ContainerSpec,
    DeploymentSchema,
    DeploymentSpec,
    EnvironmentVariable,
    TargetResource,
)
from flock_deployer.schemas.job import BaseMetaData, CronJobSchema, JobSchema


class ManifestCreator(BaseManifestCreator):
    """manifest creator"""

    def create_deployment(
        self,
        name,
        namespace,
        target_manifest: BaseFlockSchema,
    ) -> DeploymentSchema:
        """Create deployment manifest"""

        manifest = DeploymentSchema(
            apiVersion="flock/v1",
            kind="FlockDeployment",
            namespace=namespace,
            metadata=BaseMetaData(
                name=name,
                description=target_manifest.metadata.description,
                labels=target_manifest.metadata.labels,
            ),
            spec=DeploymentSpec(
                targetResource=TargetResource(  # type: ignore
                    kind=target_manifest.kind,
                    name=target_manifest.metadata.name,
                    namespace=target_manifest.namespace,
                    # description=target_manifest.metadata.description,
                    # options=target_manifest.spec.options,
                    # TODO: i have no idea why description and options must be included here by pylance if it's optional in the schema
                ),
                replicas=1,
                container=ContainerSpec(
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
                ),
            ),
        )

        return manifest

    def fetch_image(self, target_kind: str):
        """Fetch image name dynamically based on target kind from system configuration"""
        # TODO: make it actually dynamic, from some global configuration

        if target_kind == "Agent":
            return "flock-agent:latest"
        if target_kind == "EmbeddingsLoader":
            return "flock-embeddings-loader:latest"
        if target_kind == "WebScraper":
            return "flock-web-scraper:latest"

        raise NotImplementedError

    def fetch_env_vars(
        self, target_manifest: BaseFlockSchema
    ) -> List[EnvironmentVariable]:
        """Fetch env vars dynamically"""
        target_kind = target_manifest.kind
        result = []

        if target_kind == "Agent":
            result = (
                result
                + self.fetch_resource_store_env_vars()
                + self.fetch_api_tokens_env_vars(target_manifest)
                + [
                    EnvironmentVariable(  # type: ignore
                        name="FLOCK_AGENT_HOST",
                        value="0.0.0.0",
                    )
                ]
            )

        return result

    def fetch_resource_store_host(self) -> str:
        """Fetch resource store host dynamically from system configuration"""
        # TODO: make it actually dynamic, will fetch it from global configuration

        return "flock-resource-store"

    def fetch_resource_store_env_vars(self) -> List[EnvironmentVariable]:
        """Fetch resource-store env vars dynamically from system configuration"""
        # TODO: make it actually dynamic, will fetch it from global configuration

        return [
            EnvironmentVariable(  # type: ignore
                name="RESOURCE_STORE_USERNAME",
                value="root",
                # valueFrom={
                #     "secretKeyRef": {
                #         "name": "mysecret",
                #         "key": "mongo-username",
                #     }
                # },
            ),
            EnvironmentVariable(  # type: ignore
                name="RESOURCE_STORE_PASSWORD",
                value="password",
                # valueFrom={
                #     "secretKeyRef": {
                #         "name": "mysecret",
                #         "key": "mongo-password",
                #     }
                # },
            ),
            EnvironmentVariable(  # type: ignore
                name="RESOURCE_STORE_HOST",
                value=self.fetch_resource_store_host(),
            ),
        ]

    def fetch_api_tokens_env_vars(
        self,
        target_manifest: BaseFlockSchema,
    ) -> List[EnvironmentVariable]:
        """Fetch api tokens env vars dynamically from system configuration"""

        env_vars = []

        # TODO: This is a temporary solution, will be replaced with a more generic dynamic solution.
        # should pull a specific secrets set globally previously by the user
        # how does it will know which one to pull? search in the target manifest, then recursively in the resources manifests for vendors. and by that you will know which secrets should be pulled.
        # so the search can be similar, but maybe just more deep, and recursive.
        if "openai" in str(target_manifest).lower():
            env_vars.append(
                EnvironmentVariable(  # type: ignore
                    name="OPENAI_API_KEY",
                    valueFrom={
                        "secretKeyRef": {"name": "mysecret", "key": "openai-token"}
                    },
                )
            )

        if "search" in str(target_manifest).lower():
            env_vars.append(
                EnvironmentVariable(  # type: ignore
                    name="SERPAPI_API_KEY",
                    valueFrom={
                        "secretKeyRef": {
                            "name": "mysecret",
                            "key": "serpapi-token",
                        }
                    },
                )
            )

        return env_vars

        # def create_job()
        # def create_cronjob()
