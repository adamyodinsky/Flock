from abc import ABC, abstractmethod

from pydantic import BaseModel


class DetailsModel(BaseModel):
    name: str
    kind: str
    phase: str
    namespace: str
    ip: str
    host_ip: str
    node_name: str


class LogsModel(BaseModel):
    name: str
    logs: str


class MetricsModel(BaseModel):
    name: str
    namespace: str
    cpu_usage: str
    memory_usage: str


class Observer(ABC):
    @abstractmethod
    def metrics(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> list[MetricsModel]:
        pass

    @abstractmethod
    def details(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> list[DetailsModel]:
        pass

    @abstractmethod
    def logs(
        self, kind: str = "", namespace: str = "", name: str = ""
    ) -> list[LogsModel]:
        pass
