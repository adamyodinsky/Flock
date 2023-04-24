from _typeshed import Incomplete
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Literal, Optional

class Kind(str, Enum):
    Embedding: str
    VectorStore: str
    VectorStoreQATool: str
    LLM: str
    LoadTool: str
    Splitter: str
    Agent: str
    PromptTemplate: str
    LLMTool: str
    Custom: str

class BaseModelConfig(BaseModel):
    class Config:
        validate_all: bool
        extra: Incomplete

class BaseAnnotations(BaseModelConfig):
    annotations: Optional[dict[str, str]]

class BaseLabels(BaseModelConfig):
    labels: Optional[dict[str, str]]

class BaseDependency(BaseLabels):
    name: str
    kind: Kind
    namespace: Optional[str]

class BaseMetaData(BaseLabels, BaseAnnotations):
    name: str
    description: str

class BaseNamespace(BaseModelConfig):
    namespace: Optional[str]

class BaseOptions(BaseModelConfig):
    options: Optional[dict]

class BaseSpec(BaseOptions):
    vendor: str
    dependencies: Optional[List[BaseDependency]]

class BaseFlockSchema(BaseNamespace):
    apiVersion: Literal['flock/v1']
    metadata: BaseMetaData
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    spec: BaseSpec
