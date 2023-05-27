"""Validate all schemas in the schemas folder."""

from typing import Any, Dict

from flock_common.validation import validation_iterator

from flock_schemas import SchemasFactory


def validate_schema(data: Dict[str, Any]):
    """Validate all CRDs in a file."""

    kind = data["kind"]
    scheme = SchemasFactory.get_schema(kind)
    schema_instance = scheme.validate(data)
    print(schema_instance.__str__())


validation_iterator("../schemas_core", validate_schema)
validation_iterator("../schemas_deployments", validate_schema)
