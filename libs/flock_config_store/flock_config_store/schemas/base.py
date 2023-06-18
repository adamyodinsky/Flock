from typing import Optional

from pydantic import BaseModel


class SecretKeyRef(BaseModel):
    name: str
    key: str


class Env(BaseModel):
    name: str
    value: Optional[str] = None
    valueFrom: Optional[SecretKeyRef] = None


class Metadata(BaseModel):
    name: str
    description: str


class DeploymentConfig(BaseModel):
    apiVersion: str
    kind: str
    metadata: Metadata
    env: list[Env]
