"""Main module for the Flock Orchestrator server."""

import logging
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars, init_logging
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory

from flock_deployer.api import get_router
from flock_deployer.config_store import ConfigStoreFactory
from flock_deployer.deployer import DeployerFactory

init_logging()
load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))

required_vars = []
optional_vars = ["FLOCK_DEPLOYER_TYPE"]
check_env_vars(required_vars, optional_vars)

app = FastAPI(
    title="Flock",
    description="Flock Orchestrator",
    version="0.0.1",
)

logging.info("Initializing Flock Resource Store")
resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.environ.get("FLOCK_RESOURCE_STORE_TYPE", "mongo"),
    db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
    host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
    port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
    username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
    password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
)

logging.info("Initializing Flock Secret Store")
secret_store = SecretStoreFactory.get_secret_store(
    store_type=os.environ.get("SECRET_STORE_TYPE", "vault"),
    host=os.environ.get("SECRET_STORE_HOST", "localhost"),
    token=os.environ.get("SECRET_STORE_TOKEN", "root"),
)

logging.info("Initializing Flock Config Store")
config_store = ConfigStoreFactory.get_store(
    store_type=os.environ.get("CONFIG_STORE_TYPE", "mongo"),
    db_name=os.environ.get("CONFIG_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("CONFIG_STORE_TABLE_NAME", "flock_configs"),
    host=os.environ.get("CONFIG_STORE_HOST", "localhost"),
    port=int(os.environ.get("CONFIG_STORE_PORT", 27017)),
    username=os.environ.get("CONFIG_STORE_USERNAME", "root"),
    password=os.environ.get("CONFIG_STORE_PASSWORD", "password"),
)

logging.info("Initializing Flock Deployer")
deployers = DeployerFactory.get_deployer(
    deployer_type=os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"),
    secret_store=secret_store,
    resource_store=resource_store,
    config_store=config_store,
)


router = get_router(deployers)
app.include_router(router)
