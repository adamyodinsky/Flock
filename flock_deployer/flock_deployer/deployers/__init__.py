"""Module for creating deployers."""

from flock_deployer.deployers.base import BaseDeployer
from flock_deployer.deployers.k8s.k8s_deployer import K8sDeployer


class DeployerFactory:
    """Factory class for creating deployers."""

    DEPLOYERS = {"k8s": K8sDeployer}

    @staticmethod
    def get_deployer(deployer_type: str) -> BaseDeployer:
        """Factory function for creating a deployer."""

        if deployer_type == "k8s":
            return K8sDeployer()
        else:
            raise ValueError(f"Unsupported deployer type: {deployer_type}")
