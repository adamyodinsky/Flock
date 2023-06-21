import os

from flock_common.env_checker import check_env_vars

from flock_task_management_store.base import TaskManagementStore
from flock_task_management_store.mongo import MongoTaskManagementStore


class TaskManagementStoreFactory:
    """Factory class for TaskManagementStore"""

    Stores = {"mongo": MongoTaskManagementStore}

    @staticmethod
    def get_store(store_type: str = "mongo", **kwargs) -> TaskManagementStore:
        # Check env vars
        required_vars = []
        optional_vars = ["FLOCK_MANAGEMENT_STORE_TYPE"]
        check_env_vars(required_vars, optional_vars)
        store: TaskManagementStore = NotImplemented

        try:
            store = TaskManagementStoreFactory.Stores[
                os.environ.get("FLOCK_MANAGEMENT_STORE_TYPE", store_type)
            ](**kwargs)
        except KeyError as error:
            raise ValueError(f"Invalid store type: {store_type}") from error

        return store
