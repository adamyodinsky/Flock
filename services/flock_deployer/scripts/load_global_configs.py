import os

from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory

from flock_deployer.config_store.factory import ConfigStoreFactory
from flock_deployer.deployer import DeployerFactory
from flock_deployer.schemas.config import DeploymentConfigSchema

os.environ["LOCAL"] = "true"
PATH = "./assets/schemas/configs"

resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.environ.get("RESOURCE_STORE_TYPE", "mongo"),
    db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
    host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
    port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
    username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
    password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
)

secret_store = SecretStoreFactory.get_secret_store(
    store_type=os.environ.get("SECRET_STORE_TYPE", "vault"),
    host=os.environ.get("SECRET_STORE_HOST", "http://localhost:8200"),
    token=os.environ.get("SECRET_STORE_TOKEN", "root"),
)

config_store = ConfigStoreFactory.get_store(
    store_type=os.environ.get("CONFIG_STORE_TYPE", "mongo"),
    db_name=os.environ.get("CONFIG_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("CONFIG_STORE_TABLE_NAME", "flock_configs"),
    host=os.environ.get("CONFIG_STORE_HOST", "localhost"),
    port=int(os.environ.get("CONFIG_STORE_PORT", 27017)),
    username=os.environ.get("CONFIG_STORE_USERNAME", "root"),
    password=os.environ.get("CONFIG_STORE_PASSWORD", "password"),
)


deployers = DeployerFactory.get_deployer(
    deployer_type=os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"),
    secret_store=secret_store,
    resource_store=resource_store,
    config_store=config_store,
)

for file_name in os.listdir(PATH):
    print("Loading file: ", file_name, end=" ", flush=True)
    global_config = config_store.load_file(path=f"{PATH}/{file_name}")
    global_config = DeploymentConfigSchema.validate(global_config)
    config_store.put(global_config.dict())
    print("OK")
