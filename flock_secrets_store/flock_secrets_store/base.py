"""Secrets store base class. This class is used to save and load secrets."""

import abc
from typing import Any


class SecretStore(metaclass=abc.ABCMeta):
    """Abstract base class for entity stores."""

    def __init__(self, app_name: str = "flock") -> None:
        """Initialize the secret store."""
        self.app_name = app_name
        self.secret_path = f"kv/secrets/{app_name}"

    @abc.abstractmethod
    def get(self, key: str, version: int = None) -> Any:
        """Get a secret by key."""
        pass

    @abc.abstractmethod
    def put(self, key: str, value: Any) -> None:
        """Put a secret with a specific key."""
        pass

    @abc.abstractmethod
    def list_versions(self, key: str) -> dict:
        """List all versions of a specific secret."""
        pass
