"""Base class for a deployer"""

import abc

from flock_schemas.deployment import DeploymentSchema


class BaseDeployer(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    @abc.abstractmethod
    def deploy(self, manifest: DeploymentSchema):
        """deploy a manifest"""

    @abc.abstractmethod
    def stop(self, manifest: DeploymentSchema):
        """stop a manifest"""

    @abc.abstractmethod
    def kill(self, manifest: DeploymentSchema):
        """kill a manifest"""
