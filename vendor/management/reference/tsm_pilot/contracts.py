"""Strict JSON and structural validation for the experimental profile."""

from datetime import datetime, timezone
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


class ContractError(ValueError):
    """The supplied record does not meet the pilot contract."""


def timestamp(value: str) -> datetime:
    if value.endswith("-00:00"):
        raise ValueError("Unknown timezone offset is not supported")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Explicit timezone required")
    return parsed.astimezone(timezone.utc)


FORMATS = FormatChecker()


@FORMATS.checks("date-time", raises=(ValueError, TypeError, AttributeError))
def valid_time(value):
    timestamp(value)
    return True


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise ContractError(f"Non-finite JSON number: {value}")


def _float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ContractError("JSON number exceeds the supported finite range")
    return number


def loads(content: str):
    try:
        return json.loads(content, object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_float)
    except (ValueError, TypeError) as error:
        raise ContractError(str(error)) from error


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas/pilot-v0.1.schema.json"
SCHEMA = loads(SCHEMA_PATH.read_text(encoding="utf-8"))
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FORMATS)


def validate(record: dict) -> dict:
    try:
        clean = loads(json.dumps(record, allow_nan=False))
    except (ValueError, TypeError) as error:
        raise ContractError(str(error)) from error
    errors = list(VALIDATOR.iter_errors(clean))
    if errors:
        error = errors[0]
        path = ".".join(str(part) for part in error.absolute_path) or "record"
        raise ContractError(f"{path}: {error.message}")
    return clean


def ref(record: dict) -> dict:
    return {"id": record["id"], "version": record["version"]}
