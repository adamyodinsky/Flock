"""API module for the Flock Observer service. This module contains the API router and endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException

from flock_observer.observer import DetailsModel, LogsModel, MetricsModel, Observer


def get_router(observer: Observer) -> APIRouter:
    """Get API router"""

    logging.info("Creating API router")
    router = APIRouter()

    @router.get("/health")
    @router.get("/")
    async def health_endpoint():
        """Health endpoint

        Check the health of the deployer.

        Args:


        Returns:
            dict: Health status

        """

        logging.info("Checking health")

        return {"status": "OK"}

    @router.get("/metrics/{kind}/{namespace}/{name}")
    @router.get("/metrics/{kind}/{namespace}")
    @router.get("/metrics/{kind}")
    @router.get("/metrics/{namespace}")
    @router.get("/metrics")
    async def metrics_endpoint(
        kind: str = "",
        namespace: str = "",
        name: str = "",
        observer: Observer = Depends(lambda: observer),
    ) -> list[MetricsModel]:
        """Metrics endpoint

        Get metrics by a filter name, namespace and kind

        Args:
            kind (str, optional): The kind to filter by. Defaults to "".
            namespace (str, optional): The namespace to filter by. Defaults to "".
            name (str, optional): The name to filter by. Defaults to "".

        Returns:
            list[MetricsModel]: List of metrics

        """

        logging.info("Getting metrics")

        try:
            metrics = observer.metrics(kind, namespace, name)
        except Exception:
            logging.exception("Failed to get metrics")
            raise HTTPException(status_code=500, detail="Failed to get metrics")

        return metrics

    @router.get("/details/{kind}/{namespace}/{name}")
    @router.get("/details/{kind}/{namespace}")
    @router.get("/details/{kind}")
    @router.get("/details/{namespace}")
    @router.get("/details")
    async def details_endpoint(
        kind: str = "",
        namespace: str = "",
        name: str = "",
        observer: Observer = Depends(lambda: observer),
    ) -> list[DetailsModel]:
        """Details endpoint

        Get details by a filter name, namespace and kind

        Args:
            kind (str, optional): The kind to filter by. Defaults to "".
            namespace (str, optional): The namespace to filter by. Defaults to "".
            name (str, optional): The name to filter by. Defaults to "".

        Returns:
            list[DetailsModel]: List of details

        """

        logging.info("Getting details")

        try:
            details = observer.details(kind, namespace, name)
        except Exception:
            logging.exception("Failed to get details")
            raise HTTPException(status_code=500, detail="Failed to get details")

        return details

    @router.get("/logs/{kind}/{namespace}/{name}")
    @router.get("/logs/{kind}/{namespace}")
    @router.get("/logs/{kind}")
    @router.get("/logs/{namespace}")
    @router.get("/logs")
    async def logs_endpoint(
        kind: str = "",
        namespace: str = "",
        name: str = "",
        observer: Observer = Depends(lambda: observer),
    ) -> list[LogsModel]:
        """Logs endpoint

        Get logs by a filter name, namespace and kind

        Args:
            kind (str, optional): The kind to filter by. Defaults to "".
            namespace (str, optional): The namespace to filter by. Defaults to "".
            name (str, optional): The name to filter by. Defaults to "".

        Returns:
            list[LogsModel]: List of logs

        """

        logging.info("Getting logs")

        try:
            logs = observer.logs(kind, namespace, name)
        except Exception:
            logging.exception("Failed to get logs")
            raise HTTPException(status_code=500, detail="Failed to get logs")

        return logs

    return router
