from flock_resource_store import ResourceStore
from flock_schemas.deployment import DeploymentSchema
from flock_schemas.job import CronJobSchema, JobSchema

from flock_deployer.manifest_creator.base import BaseManifestCreator


class K8sManifestCreator(BaseManifestCreator):
    """K8s manifest creator"""

    def create(self, name, namespace, target):
        """Create manifest"""
        if isinstance(target, DeploymentSchema):
            return self._create_deployment(name, namespace, target)
        # if isinstance(target, JobSchema):
        #     return self._create_job(name, namespace, target)
        # if isinstance(target, CronJobSchema):
        #     return self._create_cronjob(name, namespace, target)
        raise NotImplementedError(f"Unknown target type {type(target)}")

    def _create_deployment(self, name, namespace, target) -> DeploymentSchema:
        """Create deployment manifest"""
        manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": name,
                "namespace": namespace,
                "labels": {
                    "app": name,
                },
            },
            "spec": {
                "replicas": target.replicas,
                "selector": {
                    "matchLabels": {
                        "app": name,
                    },
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": name,
                        },
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": name,
                                "image": target.image,
                                "imagePullPolicy": target.image_pull_policy,
                                "ports": [
                                    {
                                        "containerPort": target.container_port,
                                    },
                                ],
                                "env": [
                                    {
                                        "name": secret.name,
                                        "valueFrom": {
                                            "secretKeyRef": {
                                                "name": secret.secret_name,
                                                "key": secret.key,
                                            },
                                        },
                                    }
                                    for secret in target.secrets
                                ],
                            },
                        ],
                    },
                },
            },
        }
        return manifest
