"""Entirely synthetic examples. Values are not model or human study results."""

from datetime import datetime, timedelta, timezone


class FixtureClock:
    def __init__(self):
        self.value = datetime(2026, 10, 2, 12, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += timedelta(seconds=seconds)


def experiment_spec(baseline_id, candidate_id):
    return {
        "schemaVersion": "tsev-pilot/0.1",
        "hypothesis": "An evidence-first drafting prompt improves quality while preserving review judgment and effort.",
        "baselineRef": baseline_id,
        "candidateRef": candidate_id,
        "population": "synthetic-support-cases-v1",
        "method": "synthetic-rubric-v1",
        "windowStart": "2026-10-02T09:00:00Z",
        "windowEnd": "2026-10-02T11:00:00Z",
        "reviewBefore": "2026-10-03T12:00:00Z",
        "maxAgeSeconds": 7200,
        "minCases": 20,
        "criteria": [
            {"metric": "quality", "unit": "percent", "direction": "higher", "minimumGain": 5, "candidateLimit": 85},
            {"metric": "human_detection", "unit": "percent", "direction": "higher", "minimumGain": 0, "candidateLimit": 80},
            {"metric": "review_minutes", "unit": "minutes", "direction": "lower", "minimumGain": 0, "candidateLimit": 6},
        ],
        "limitations": "Synthetic aggregate values; count is a completeness guard, not statistical power or a real study.",
    }


BASELINE_VALUES = {"quality": 80, "human_detection": 85, "review_minutes": 5}
SUPPORTED_VALUES = {"quality": 90, "human_detection": 90, "review_minutes": 4.5}
FAST_UNSAFE_VALUES = {"quality": 90, "human_detection": 70, "review_minutes": 3}


def add_observation(pilot, experiment, config_id, metric, value, **overrides):
    spec = experiment["spec"]
    criterion = next(c for c in spec["criteria"] if c["metric"] == metric)
    fields = {
        "experiment_id": experiment["id"], "config_id": config_id, "metric": metric,
        "value": value, "cases": 20, "population": spec["population"], "method": spec["method"],
        "unit": criterion["unit"], "window_start": spec["windowStart"], "window_end": spec["windowEnd"],
        "observed_at": "2026-10-02T11:30:00Z", "source": "synthetic-fixture",
        "limitations": "Fabricated measurement for a control-flow demonstration; no human or AI was evaluated.",
    }
    fields.update(overrides)
    return pilot.observe(**fields)


def fill_evidence(pilot, experiment, candidate_values=None, overrides=None):
    candidate_values = SUPPORTED_VALUES if candidate_values is None else candidate_values
    overrides = {} if overrides is None else overrides
    for ref, values in ((experiment["spec"]["baselineRef"], BASELINE_VALUES),
                        (experiment["spec"]["candidateRef"], candidate_values)):
        for metric, value in values.items():
            add_observation(pilot, experiment, ref, metric, value, **overrides)


def seed(pilot):
    baseline = pilot.add_config("Baseline", "Fixture: draft a response; human reviews and sends.")
    candidate = pilot.add_config("Evidence-first candidate", "Fixture: cite the basis, flag uncertainty, and leave sending to a human.")
    pilot.bootstrap(baseline["id"])
    experiment = pilot.add_experiment(experiment_spec(baseline["id"], candidate["id"]))
    return baseline, candidate, experiment
