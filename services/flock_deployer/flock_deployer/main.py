"""Main module for the Flock Orchestrator server."""

import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory

from flock_deployer.api import get_router
from flock_deployer.deployer import DeployerFactory

load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))

required_vars = ["FLOCK_DEPLOYER_TYPE"]
optional_vars = []
check_env_vars(required_vars, optional_vars)

app = FastAPI(
    title="Flock",
    description="Flock Orchestrator",
    version="0.0.1",
)


resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.environ.get("FLOCK_RESOURCE_STORE_TYPE", "mongo"),
    db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
    table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
    host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
    port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
    username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
    password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
)


secret_store = SecretStoreFactory.get_secret_store("vault")

deployers = DeployerFactory.get_deployer(
    deployer_type=os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"),
    secret_store=secret_store,
    resource_store=resource_store,
)


router = get_router(deployers)
app.include_router(router)
