"""Base class for a deployer"""

import abc

from flock_schemas import BaseFlockSchema
from flock_schemas.deployment import DeploymentSchema
from flock_secrets_store import SecretStore


class BaseDeployer(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    def __init__(self, secret_store: SecretStore) -> None:
        self.secret_store: SecretStore = secret_store

    @abc.abstractmethod
    def deploy(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Deploy"""

    @abc.abstractmethod
    def delete(
        self, manifest: DeploymentSchema, target_manifest: BaseFlockSchema, dry_run=None
    ):
        """Delete"""
