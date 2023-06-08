import unittest

from mongomock import MongoClient as MockMongoClient
from pymongo import MongoClient
from store.mongo import MongoResourceStore


class TestMongoResourceStore(unittest.TestCase):
    def setUp(self):
        # Use mongomock to create a mock MongoClient
        self.mock_client = MockMongoClient()
        self.mock_store = MongoResourceStore(
            db_name="test_db",
            collection_name="test_collection",
            client=self.mock_client,
        )

        # Configure this with your actual MongoDB instance for integration testing
        self.real_client = MongoClient("mongodb://root:your_password@localhost:27017")
        self.real_store = MongoResourceStore(
            db_name="test_db",
            collection_name="test_collection",
            client=self.real_client,
        )

    def tearDown(self):
        # Drop the test collection after each test
        self.real_store.collection.drop()

    def test_integration(self):
        """Integration test for MongoResourceStore"""

        for store in [self.mock_store, self.real_store]:
            self._test_put_get_delete(store)

    def _test_put_get_delete(self, store):
        key = "example_namespace/example_kind/example_name"
        value = {"data": "test_value"}

        # Test put
        store.put(key, value)
        stored_value = store.get(key)
        self.assertIsNotNone(stored_value)
        self.assertEqual(value["data"], stored_value["data"])

        # Test update
        updated_value = {"data": "updated_value"}
        store.put(key, updated_value)
        stored_value = store.get(key)
        self.assertIsNotNone(stored_value)
        self.assertEqual(updated_value["data"], stored_value["data"])

        # Test delete
        store.delete(key)
        stored_value = store.get(key)
        self.assertIsNone(stored_value)


if __name__ == "__main__":
    unittest.main()
