"""Package to store and retrieve secrets from secret store"""

from flock_secrets_store.base import SecretStore
from flock_secrets_store.vault import VaultSecretStore

# secret store factory


class SecretStoreFactory:
    """Factory class to create secret store"""

    @staticmethod
    def get_secret_store(secret_store_type) -> SecretStore:
        """Returns secret store object based on secret store type"""
        if secret_store_type == "vault":
            return VaultSecretStore
        else:
            raise ValueError(f"Unknown secret store type: {secret_store_type}")
