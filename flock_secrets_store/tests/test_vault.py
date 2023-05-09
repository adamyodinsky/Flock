import unittest

from vault_secret_store import VaultSecretStore

# Replace these placeholders with appropriate values
vault_url = "https://vault.example.com:8200"
token = "your_vault_token_here"


class TestVaultSecretStore(unittest.TestCase):
    def setUp(self):
        self.vault_secret_store = VaultSecretStore(vault_url, token)

    def test_store_and_fetch_secret(self):
        test_path = "test-secrets"
        test_secret_name = "test_api_key"
        test_secret_data = {"key": "abcdef"}

        # Store the test secret
        self.vault_secret_store.store_secret(
            test_path, test_secret_name, test_secret_data
        )

        # Fetch the test secret
        fetched_secret_data = self.vault_secret_store.fetch_secret(
            test_path, test_secret_name
        )

        # Assert the fetched secret data matches the stored data
        self.assertEqual(test_secret_data, fetched_secret_data)

    def test_fetch_non_existent_secret(self):
        test_path = "test-secrets"
        test_secret_name = "non_existent_secret"

        # Fetch the non-existent secret
        fetched_secret_data = self.vault_secret_store.fetch_secret(
            test_path, test_secret_name
        )

        # Assert the fetched secret data is None
        self.assertIsNone(fetched_secret_data)

    def test_secret_engine_enabled(self):
        test_path = "test-secrets"

        # Enable the KV engine at the test path
        self.vault_secret_store.enable_kv_engine(test_path)

        # Check if the secret engine is enabled
        is_enabled = self.vault_secret_store.check_secret_engine_enabled(test_path)

        # Assert the secret engine is enabled
        self.assertTrue(is_enabled)


if __name__ == "__main__":
    unittest.main()
