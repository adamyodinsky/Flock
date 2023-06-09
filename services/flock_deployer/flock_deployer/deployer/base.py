"""Base class for a deployer"""

import abc

from flock_common.secret_store import SecretStore

from flock_deployer.schemas.base import BaseFlockSchema


class BaseDeployer(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    def __init__(self, secret_store: SecretStore) -> None:
        self.secret_store: SecretStore = secret_store

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

    def __init__(self, secret_store: SecretStore) -> None:
        """Initialize the deployer"""

        self.service_deployer: BaseDeployer
        self.deployment_deployer: BaseDeployer
        self.cron_job_deployer: BaseDeployer
        self.job_deployer: BaseDeployer
