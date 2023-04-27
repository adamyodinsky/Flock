# coding: utf-8

from typing import List

from fastapi import Depends, Security  # noqa: F401
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows  # noqa: F401
from fastapi.security import (
    HTTPAuthorizationCredentials,  # noqa: F401
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.security.api_key import (
    APIKeyCookie,
    APIKeyHeader,  # noqa: F401
    APIKeyQuery,
)

from server.models.extra_models import TokenModel
