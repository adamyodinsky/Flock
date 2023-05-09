"""A module for storing and retrieving secrets from Vault."""

import hvac
from hvac.exceptions import InvalidPath, VaultError


class VaultSecretStore:
    """A class for storing and retrieving secrets from Vault."""

    def __init__(self, vault_url, token):
        self.client = hvac.Client(url=vault_url, token=token)

    def check_secret_engine_enabled(self, path):
        """Check if the secret engine is enabled at the given path."""
        secret_engines = self.client.sys.list_mounted_secrets_engines()

        # Ensure the path has a trailing slash
        path_with_slash = path if path.endswith("/") else f"{path}/"

        return path_with_slash in secret_engines

    def enable_kv_engine(self, path, version=2):
        """Enable the KV engine at the given path if it's not already enabled."""
        if not self.check_secret_engine_enabled(path):
            self.client.sys.enable_secrets_engine(
                backend_type="kv", path=path, options={"version": version}
            )

    def put(self, path, secret_name, secret_data):
        """Store a secret in the Vault KV engine."""
        try:
            self.enable_kv_engine(path)
            secret_path = f"{path}/data/{secret_name}"
            self.client.secrets.kv.v2.create_or_update_secret(
                path=secret_path, secret=secret_data
            )
        except InvalidPath as error:
            print(f"Invalid path for storing secret: {error}")
        except VaultError as error:
            print(f"Error storing secret: {error}")

    def get(self, path, secret_name):
        """Fetch a secret from the Vault KV engine."""
        try:
            secret_path = f"{path}/data/{secret_name}"
            response = self.client.secrets.kv.v2.read_secret_version(path=secret_path)
            return response["data"]["data"]
        except InvalidPath as error:
            print(f"Invalid path for fetching secret: {error}")
            return None
        except VaultError as error:
            print(f"Error fetching secret: {error}")
            return None
