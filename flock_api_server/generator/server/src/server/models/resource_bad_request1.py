# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from server.models.code5 import Code5
from server.models.status1 import Status1


class ResourceBadRequest1(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ResourceBadRequest1 - a model defined in OpenAPI

        status: The status of this ResourceBadRequest1 [Optional].
        code: The code of this ResourceBadRequest1 [Optional].
        message: The message of this ResourceBadRequest1 [Optional].
        details: The details of this ResourceBadRequest1 [Optional].
    """

    status: Optional[Status1] = Field(alias="status", default=None)
    code: Optional[Code5] = Field(alias="code", default=None)
    message: Optional[str] = Field(alias="message", default=None)
    details: Optional[List[str]] = Field(alias="details", default=None)

ResourceBadRequest1.update_forward_refs()
