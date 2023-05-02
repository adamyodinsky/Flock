"""Validate all schemas in the schemas folder."""

from typing import Any, Dict

from flock_common.validation import validation_iterator

from flock_schemas import SchemasFactory

# from pydantic import ValidationError


def validate_schema(data: Dict[str, Any]):
    """Validate all CRDs in a file."""

    kind = data["kind"]
    scheme = SchemasFactory.get_schema(kind)
    scheme.validate(data)


validation_iterator("../schemas_core", validate_schema)
