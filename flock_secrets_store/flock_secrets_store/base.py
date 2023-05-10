"""Secrets store base class. This class is used to save and load secrets."""

import abc


class SecretStore(metaclass=abc.ABCMeta):
    """Abstract base class for entity stores."""

    def __init__(self, url="", token="", app_name="flock") -> None:
        """Initialize the secret store."""
        self.app_name = app_name

    @abc.abstractmethod
    def put(self, path, secret_name, secret_data):
        """Put a secret with a specific key."""

    @abc.abstractmethod
    def get(self, path, secret_name):
        """Get a secret by key."""
