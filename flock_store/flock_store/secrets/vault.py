"""Vault secret store implementation."""

from typing import Any

import hvac

from flock_store.secrets.base import SecretStore


class VaultSecretStore(SecretStore):
    def __init__(self, vault_addr: str, vault_token: str, app_name: str = "flock"):
        super().__init__(app_name)
        self.client = hvac.Client(url=vault_addr, token=vault_token)

        if not self.client.is_authenticated():
            raise ValueError("Invalid Vault token")

    def get(self, key: str, version: int = None):
        read_params = {"version": version} if version else {}
        secret_response = self.client.read(f"{self.secret_path}/{key}", **read_params)
        if secret_response is None:
            raise ValueError(f"No secret found for key: {key}")
        return secret_response["data"]["data"]["value"]

    def put(self, key: str, value: Any):
        self.client.write(f"{self.secret_path}/{key}", data={"value": value})

    def list_versions(self, key: str):
        secret_metadata = self.client.read(f"kv/metadata/{self.app_name}/{key}")
        if secret_metadata is None:
            raise ValueError(f"No metadata found for key: {key}")
        return secret_metadata["data"]["versions"]
