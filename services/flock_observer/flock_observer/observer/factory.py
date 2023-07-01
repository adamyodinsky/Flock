import logging

from flock_observer.observer.base import Observer
from flock_observer.observer.k8s import K8sObserver


class ObserverFactory:
    """Observer factory"""

    OBSERVERS = {"k8s": K8sObserver}

    def __init__(self) -> None:
        """Initialize the Observer factory"""

        logging.debug("Initializing ObserverFactory")

    def get_observer(self, observer_type: str, **kwargs) -> Observer:
        """Get an Observer

        Returns:
            Observer: An Observer
        """

        logging.info("Getting Observer")

        if observer_type in self.OBSERVERS:
            return self.OBSERVERS[observer_type](**kwargs)
        else:
            raise Exception(f"Unknown Observer type: {observer_type}")
