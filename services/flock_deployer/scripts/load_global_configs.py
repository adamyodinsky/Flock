from flock_deployer.config_store.base import ConfigStore
from flock_deployer.config_store.factory import ConfigStoreFactory

config_store = ConfigStoreFactory.get_store("mongo")
