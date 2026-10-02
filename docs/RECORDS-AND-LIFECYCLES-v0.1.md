# Records and lifecycles v0.1

Status: proposed general semantics. The [pilot profile](../schemas/README.md) is narrower.

## Common conventions

Use stable identities and immutable material versions. Separate schema version, business revision, artifact digest, deployment identity, and assessment revision. Record scope, owner, producer, observation and recording times with explicit timezones, references, limitations, and supersession. An identifier or digest proves neither access permission nor truth.

## Minimal learning case

| Record | Required meaning |
|---|---|
| Baseline | Configuration and environment, measured state or explicit unknown, population, method, period, limitations |
| LearningRecord | Management-compatible assumption, supporting/contrary evidence, assessment, applicability, proposed decision impact |
| Experiment | Hypothesis, baseline/candidate bindings, protocol, population, criteria, limits, owner, participation and data conditions |
| Observation | Exact subject and method, source, period, value or missing state, sample basis, availability and limitations |
| Evaluation | Evidence snapshot, findings per criterion, comparability, contradictions, uncertainty, scope of supported claims |
| AdaptationProposal | Exact artifacts and dependencies to change, impact, evaluation, rollout scope, recovery, monitoring |
| AdoptionDecision | Management decision bound to proposal and evaluation revisions, accountable owner, conditions, alternatives, rationale |
| ActivationRecord | Engineering action and observed state, exact artifact, authority, expected prior state, verification, subsequent recovery links |

Signals, reflections, and hypotheses may be embedded in the learning case. Monitoring reviews and retirement records may reuse Management reviews. An `EvolutionLineage` is a view over links; it does not require a separate graph database.

## Independent states

| Dimension | Proposed states |
|---|---|
| Experiment activity | proposed, authorized, running, stopped, completed |
| Evidence assessment | insufficient, supported, contradicted |
| Adoption decision | proposed, adopted, rejected, deferred, superseded |
| Activation | not-started, requested, verified, unresolved, failed |
| Monitoring | pending, acceptable, concerning, unavailable |
| Recovery | not-requested, requested, verified, unresolved, unsupported |

A completed experiment can contradict its hypothesis. An adopted change may never activate. A verified activation can cause a regression. A restored configuration may have irreversible prior effects. Preserve each fact independently.

## Relationships that matter

Bind the hypothesis and evaluation to exact versions. Preserve all considered evidence, including excluded records and their exclusion reasons. Link a correction to its predecessor. Check the latest relevant evidence and current baseline before activation. A later observation can make an earlier evaluation unsuitable for a new decision while leaving that evaluation intact as history.

Reusing a lesson requires review of its applicability: population, language, domain, model, tools, environment, and policy. References to restricted evidence do not authorize disclosure of it. Record whether missing source material limits reproduction or only further interpretation.

## Pilot mappings are explicit, not universal

The standalone host uses its own local record IDs and immutable records. The family bridge preserves Management's integer-version references and Engineering's string-version references. It publishes a `tun-family-manifest/0.1` object linking the candidate digest, evaluation/evidence binding, mandate, and organizational decision. This manifest is an implementation-specific record, not the complete general model above.

The derived Evolution decision references Management's decision. Publication status and local activation status remain separate. A later observation, revoked permission, withdrawn publication, or newer active generation may limit what can happen next without rewriting earlier records.

See [family semantics and failure limits](FAMILY-PILOT.md). Neither a matching record name nor a rendered status demonstrates general interoperability.
