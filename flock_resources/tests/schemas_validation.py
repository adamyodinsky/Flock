"""Validate all schemas in the schemas folder."""

from typing import Any, Dict

from schemas import SchemaFactory

from flock_common.validation import validation_iterator

schema_factory = SchemaFactory()


def validate_schema(data: Dict[str, Any]):
    """Validate all CRDs in a file."""

    kind = data["kind"]

    schema = schema_factory.get_schema(kind)
    print(f"{schema.__name__} - ", flush=True, end="")
    schema_instance = schema.validate(data)


validation_iterator("schemas", validate_schema)
