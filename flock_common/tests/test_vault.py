"""Test the VaultSecretStore class."""

import os
import time
import unittest
import uuid

from flock_common.secret_store import VaultSecretStore

VAULT_URL = os.environ.get("VAULT_URL", "http://localhost:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "root")


class TestVaultSecretStore(unittest.TestCase):
    """Test the VaultSecretStore class."""

    def setUp(self):
        self.vault_secret_store = VaultSecretStore(VAULT_URL, VAULT_TOKEN)
        self.test_path = f"test-secrets-{uuid.uuid4()}"

    def tearDown(self):
        """Clean up after each test."""
        try:
            self.vault_secret_store.client.sys.disable_secrets_engine(
                path=self.test_path
            )
        except self.vault_secret_store.client.exceptions.InvalidPath:
            pass
        except Exception as error:
            print(f"Error during tearDown: {error}")

    def test_store_and_fetch_secret(self):
        """Test storing and fetching a secret."""

        test_secret_name = "test_api_key"
        test_secret_data = {"key": "abcdef"}

        # Store the test secret
        self.vault_secret_store.put(self.test_path, test_secret_name, test_secret_data)

        # Add a delay before fetching the secret
        time.sleep(1)

        # Fetch the test secret
        fetched_secret_data = self.vault_secret_store.get(
            self.test_path, test_secret_name
        )

        # Assert the fetched secret data matches the stored data
        self.assertEqual(test_secret_data, fetched_secret_data)

    def test_fetch_non_existent_secret(self):
        """Test fetching a non-existent secret."""

        test_secret_name = "non_existent_secret"

        # Fetch the non-existent secret
        fetched_secret_data = self.vault_secret_store.get(
            self.test_path, test_secret_name
        )

        # Assert the fetched secret data is None
        self.assertIsNone(fetched_secret_data)

    def test_secret_engine_enabled(self):
        """Test checking if a secret engine is enabled."""

        # Enable the KV engine at the test path
        self.vault_secret_store.enable_kv_engine(self.test_path)

        # Check if the secret engine is enabled
        is_enabled = self.vault_secret_store.check_secret_engine_enabled(self.test_path)

        # Assert the secret engine is enabled
        self.assertTrue(is_enabled)


if __name__ == "__main__":
    unittest.main()
