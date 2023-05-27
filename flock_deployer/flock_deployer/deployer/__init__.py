"""Module for creating deployers."""

from flock_secrets_store import SecretStore

from flock_deployer.deployer.base import BaseDeployers
from flock_deployer.deployer.k8s.k8s_deployer import K8sDeployer


class DeployerFactory:
    """Factory class for creating deployers."""

    DEPLOYERS = {"k8s": K8sDeployer}

    @staticmethod
    def get_deployer(
        deployer_type: str, secret_store: SecretStore = NotImplemented
    ) -> BaseDeployers:
        """Factory function for creating a deployer.

        Args:
            deployer_type (str): The type of deployer to create.
            secret_store (SecretStore): The secret store to use for the deployer.

        Raises:
            ValueError: If the deployer type is not supported.

        Returns:
            Deployer: The deployer object.
        """

        # if secret_store is NotImplemented:
        #     raise TypeError("SecretStore must be provided to create a Deployer")

        if deployer_type in DeployerFactory.DEPLOYERS:
            return DeployerFactory.DEPLOYERS[deployer_type](secret_store)

        valid_options = ", ".join(DeployerFactory.DEPLOYERS.keys())
        raise ValueError(
            f"Unsupported deployer type: {deployer_type}. Valid options are: {valid_options}"
        )
