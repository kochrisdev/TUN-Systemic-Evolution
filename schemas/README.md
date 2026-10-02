# Experimental pilot profile

The [JSON Schema](pilot-v0.1.schema.json) describes the `spec` embedded in an experiment record, not every journal record or the full general record model. Its namespace is `tsev-pilot/0.1`. No stable API or JSON ingestion service is supplied.

The Python pilot uses a [strict profile validator](../reference/tsev_pilot/contracts.py), not a JSON Schema engine. It rejects missing/unknown fields, unsupported versions, blank strings, booleans as numbers, non-finite values, duplicate metrics, and invalid time ordering. Host checks resolve actual references, permitted configuration scope, current state, evidence bindings, and transitions.

The schema is a portable documentation artifact. This bundle has not run an independent JSON Schema implementation against it. Standard JSON Schema integer semantics and format checking may differ from the intentionally narrower Python API; do not claim cross-language compatibility without testing those boundaries.

Experiment IDs and configuration references are assigned by the local host. See [fixtures](../reference/tsev_pilot/fixtures.py) for a complete generated example. Material edits create a new experiment record and require evidence and decisions bound to that new record. Observations are append-only through the API; duplicate measurements require review and make the simple evaluator insufficient. Statistical aggregation and correction/supersession workflows are not implemented in this profile.
