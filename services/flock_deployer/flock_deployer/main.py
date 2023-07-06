"""Main module for the Flock Orchestrator server."""

import logging
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars, init_logging
from flock_common.secret_store import SecretStoreFactory
from flock_resource_store import ResourceStoreFactory
from uvicorn import run

from flock_deployer.api import get_router
from flock_deployer.config_store import ConfigStoreFactory
from flock_deployer.deployer import DeployerFactory

init_logging()


def get_app():
    api_prefix = os.environ.get("API_PREFIX", "deployer")
    app = FastAPI(
        title="Flock Deployer",
        description="Flock Deployer is a service that deploys resources to a target cluster.",
        version="0.0.1",
        docs_url=f"/{api_prefix}/docs",
        redoc_url=f"/{api_prefix}/redoc",
        openapi_url=f"/{api_prefix}/openapi.json",
    )

    @app.on_event("startup")
    async def startup_event():
        load_dotenv(find_dotenv(os.environ.get("ENV_FILE", ".env")))

        required_vars = []
        optional_vars = [
            "ENV_FILE",
            "DEPLOYER_TYPE",
            "RESOURCE_STORE_TYPE",
            "RESOURCE_STORE_DB_NAME",
            "RESOURCE_STORE_TABLE_NAME",
            "RESOURCE_STORE_HOST",
            "RESOURCE_STORE_PORT",
            "RESOURCE_STORE_USERNAME",
            "RESOURCE_STORE_PASSWORD",
            "SECRET_STORE_TYPE",
            "SECRET_STORE_HOST",
            "SECRET_STORE_TOKEN",
            "CONFIG_STORE_TYPE",
            "CONFIG_STORE_DB_NAME",
            "CONFIG_STORE_TABLE_NAME",
            "CONFIG_STORE_HOST",
            "CONFIG_STORE_PORT",
            "CONFIG_STORE_USERNAME",
            "CONFIG_STORE_PASSWORD",
            "DEPLOYER_TYPE",
            "DEPLOYER_HOST",
            "DEPLOYER_PORT",
            "API_PREFIX",
        ]
        check_env_vars(required_vars, optional_vars)

        logging.info("Initializing Flock Resource Store")
        resource_store = ResourceStoreFactory.get_resource_store(
            store_type=os.environ.get("RESOURCE_STORE_TYPE", "mongo"),
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
            host=os.environ.get("SECRET_STORE_HOST", "http://localhost:8200"),
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
            deployer_type=os.environ.get("DEPLOYER_TYPE", "k8s"),
            secret_store=secret_store,
            resource_store=resource_store,
            config_store=config_store,
        )

        router = get_router(deployers, api_prefix)
        app.include_router(router)

        host = os.environ.get("DEPLOYER_HOST", "localhost")
        port = int(os.environ.get("DEPLOYER_PORT", 9000))

        logging.info(f"Starting Flock Deployer on {host}:{port}")
        logging.info(f"/docs (GET) (http://{host}:{port}/docs)")
        logging.info(f"/redoc (GET) (http://{host}:{port}/redoc)")
        logging.info("/openapi.json (GET) (http://%s:%s/openapi.json)", host, port)
        for route in router.routes:
            logging.info("%s (%s)", route.path, route.methods)  # type: ignore

    return app


def main():
    app = get_app()
    host = os.environ.get("DEPLOYER_HOST", "localhost")
    port = int(os.environ.get("DEPLOYER_PORT", 9000))
    run(app, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info"))


if __name__ == "__main__":
    main()
