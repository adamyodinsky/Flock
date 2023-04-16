import pickle
import json
from flock_entity_store.base import EntityStore
import etcd3


class EntityStoreFS(EntityStore):
    """Entity store class. This class is used to save and load entities to and from the file system."""

    def save(self, key, obj, manifest):
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"
        serialized_obj = pickle.dumps(obj)

        with open(data_key, "wb") as f:
            f.write(serialized_obj)
        with open(manifest_key, "w") as f:
            json.dump(manifest, f)

    def load(self, key):
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"

        with open(data_key, "rb") as f:
            serialized_obj = f.read()
        obj = pickle.loads(serialized_obj)
        with open(manifest_key, "r") as f:
            manifest = json.load(f)
        return obj, manifest
    
    def save_manifest(self, key, manifest):
        with open(f"{self.manifest_prefix}/{key}", "w") as f:
            json.dump(manifest, f)

    def load_manifest(self, key):
        with open(f"{self.manifest_prefix}/{key}", "r") as f:
            manifest = json.load(f)
        return manifest

    def save_data(self, key, obj):
        serialized_obj = pickle.dumps(obj)
        with open(f"{self.data_prefix}/{key}", "wb") as f:
            f.write(serialized_obj)

    def load_data(self, key):
        with open(f"{self.data_prefix}/{key}", "rb") as f:
            serialized_obj = f.read()
        obj = pickle.loads(serialized_obj)
        return obj



class EtcdStore(EntityStore):
    """Entity store class. This class is used to save and load entities to and from the file system."""

    def __init__(self, host: str ='localhost', port: int = 2379, app_name: str = "flock", key_prefix: str = ""):
        super().__init__(
            app_name=app_name,
            key_prefix=key_prefix,
            is_fs=False
            )
        
        self.etcd_client = etcd3.client(host=host, port=port)


    def save(self, key, obj, manifest):
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"

        serialized_obj = pickle.dumps(obj)
        self.etcd_client.put(data_key, serialized_obj)
        self.etcd_client.put(manifest_key, json.dumps(manifest))

    def load(self, key):
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"

        serialized_obj, _ = self.etcd_client.get(data_key)
        manifest_str, _ = self.etcd_client.get(manifest_key)

        obj = pickle.loads(serialized_obj)
        manifest = json.loads(manifest_str)
        return obj, manifest
    
    def save_manifest(self, key, manifest):
        self.etcd_client.put(f"{self.manifest_prefix}/{key}", json.dumps(manifest))

    def load_manifest(self, key):
        manifest_str, _ = self.etcd_client.get(f"{self.manifest_prefix}/{key}")
        manifest = json.loads(manifest_str)
        return manifest
    
    def save_data(self, key, obj):
        serialized_obj = pickle.dumps(obj)
        key = f"{self.data_prefix}/{key}"
        self.etcd_client.put(key, serialized_obj)

    def load_data(self, key):
        serialized_obj, _ = self.etcd_client.get(key)
        obj = pickle.loads(serialized_obj)
        return obj
    
    