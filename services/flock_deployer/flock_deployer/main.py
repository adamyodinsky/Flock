"""Main module for the Flock Orchestrator server."""

import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars

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

deployer = DeployerFactory.get_deployer(os.environ.get("FLOCK_DEPLOYER_TYPE", "k8s"))

router = get_router(deployer)
app.include_router(router)
