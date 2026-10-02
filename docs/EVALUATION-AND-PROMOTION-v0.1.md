# Evaluation and promotion v0.1

Status: proposed guidance. [Evolution review](../templates/evolution-review.md) · [Adoption decision](../templates/adoption-decision.md)

## Evaluate the claim

Check the exact baseline and candidate, comparable populations and periods, evidence availability, method and evaluator version, contamination, missingness, adverse findings, and uncertainty. State which findings support, contradict, or leave the claim unresolved. Preserve evidence outside the planned metrics when it reveals a material concern.

Use separate gates for required improvement, acceptable non-regression, human effects, data and authority, operational readiness, and monitoring/recovery. A weighted average should not allow a speed gain to cancel a violated mandatory constraint.

An evaluation reports evidence. It may recommend adoption, further testing, rejection, or deferral. Management owns the actual decision. The same person may evaluate and decide in a small team, with that overlap recorded; a second model run does not establish independence.

## Decide and activate

1. Bind the evaluation to its exact experiment revision and evidence snapshot.
2. Prepare a concrete adaptation proposal with artifacts, dependencies, scope, and recovery.
3. Record the authorized decision, alternatives, rationale, dissent, conditions, and next review.
4. Recheck new evidence, baseline state, criteria, artifact bindings, and current authority.
5. Activate through Engineering and inspect actual state before claiming activation succeeded.
6. Start the agreed monitoring; check continued benefit separately from activation success.

If evidence, criteria, candidate, baseline, or scope changes materially, return to review. Do not edit a decided proposal in place. A revoked or expired permission prevents new activation even if the evidence remains strong.

## Narrow pilot interpretation

The local evaluator compares synthetic percentages against declared thresholds and a minimum observation count. It can report `supported`, `contradicted`, or `insufficient` for those checks only. It reports all missing, conflicting, stale, and failed findings; any observed failure takes precedence over insufficiency in its summary. Passing does not demonstrate significance, causality, human learning, or generalization.

The pilot requires a fixture owner's decision and a separate activation call. The resulting local pointer change is persisted and read back. A real provider needs its own authorization, dispatch, idempotency, reconciliation, and verification contracts.
