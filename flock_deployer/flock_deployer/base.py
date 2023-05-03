"""Base class for a deployer"""

import abc


class BaseDeployer(metaclass=abc.ABCMeta):
    """Abstract class for a deployer"""

    @abc.abstractmethod
    def deploy(self, manifest):
        """deploy a manifest"""

    @abc.abstractmethod
    def stop(self, manifest):
        """stop a manifest"""

    @abc.abstractmethod
    def kill(self, manifest):
        """kill a manifest"""
