"""Strict validation for the small pilot profile, using the standard library.

This is a profile validator, not a general JSON Schema interpreter. The companion
JSON Schema documents the experiment envelope for other implementations.
"""

from datetime import datetime, timezone
import hashlib
import json
import math


class Rejected(ValueError):
    """The requested transition or record is invalid for this profile."""


def require(condition, message):
    if not condition:
        raise Rejected(message)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text")
    require(len(value) <= 4000, f"{label} exceeds the pilot limit")
    return value


def number(value, label):
    require(type(value) in (int, float) and math.isfinite(value), f"{label} must be finite numeric data")
    return value


def count(value, label, minimum=1):
    require(type(value) is int and value >= minimum, f"{label} must be an integer >= {minimum}")
    return value


def timestamp(value):
    nonempty(value, "timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Rejected("invalid timestamp") from exc
    require(parsed.tzinfo is not None, "timestamp needs an explicit timezone")
    return parsed.astimezone(timezone.utc)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def exact_fields(value, fields, label):
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == set(fields), f"{label} has missing or unsupported fields")


def validate_experiment(spec):
    exact_fields(spec, (
        "schemaVersion", "hypothesis", "baselineRef", "candidateRef", "population",
        "method", "windowStart", "windowEnd", "reviewBefore", "maxAgeSeconds",
        "minCases", "criteria", "limitations",
    ), "experiment")
    require(spec["schemaVersion"] == "tsev-pilot/0.1", "unsupported schema version")
    for field in ("hypothesis", "baselineRef", "candidateRef", "population", "method", "limitations"):
        nonempty(spec[field], field)
    require(spec["baselineRef"] != spec["candidateRef"], "baseline and candidate must differ")
    start, end, expiry = (timestamp(spec[k]) for k in ("windowStart", "windowEnd", "reviewBefore"))
    require(start < end <= expiry, "invalid experiment window or review expiry")
    count(spec["minCases"], "minCases")
    count(spec["maxAgeSeconds"], "maxAgeSeconds")
    require(isinstance(spec["criteria"], list) and 1 <= len(spec["criteria"]) <= 10,
            "provide between one and ten criteria")
    metrics = set()
    for criterion in spec["criteria"]:
        exact_fields(criterion, ("metric", "unit", "direction", "minimumGain", "candidateLimit"), "criterion")
        metric = nonempty(criterion["metric"], "metric")
        require(metric not in metrics, "duplicate criterion")
        metrics.add(metric)
        nonempty(criterion["unit"], "unit")
        require(criterion["direction"] in ("higher", "lower"), "unsupported direction")
        number(criterion["minimumGain"], "minimumGain")
        require(criterion["minimumGain"] >= 0, "minimumGain must be nonnegative")
        number(criterion["candidateLimit"], "candidateLimit")
    return spec
