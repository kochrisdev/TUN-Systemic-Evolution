# Threat model for the draft and pilots

Status: initial threat inventory, not a security assessment.

## Trust boundary

Both pilots trust their process, caller-selected fixture identities, filesystem, clock, SQLite stores, and supplied measurements. There is no production identity provider, authenticated evidence collection, tenant isolation service, or encryption layer. Application checks do not prevent a database administrator from changing history or a caller from selecting the owner fixture.

The family pilot adds separate Management, Engineering, provider, and bridge stores. Its provider is a local simulator, not an external deployment service. A bridge transaction serializes bridge calls only; it is not a transaction over every participant.

| Failure or threat | Intended response in an adopting system | Current evidence or gap |
|---|---|---|
| Candidate grades itself favorably | Identify evaluator limits; obtain evidence appropriate to the claim | Source labels and limits recorded; no evaluator executed |
| Test contamination or repeated tuning | Separate practice/tuning and assessment; disclose selection | Method references only; real validity review remains |
| Speed harms human judgment | Preserve human constraints independently | Synthetic human-regression rejection tested |
| Averages hide adverse effects | Assess relevant groups and preserve concerns | Explicit concern can block adoption; no subgroup study |
| Missing, conflicting, stale, or changed evidence | Retain uncertainty; reassess before a new action | Core binding/freshness checks and family rechecks tested |
| Feedback injects permissions | Treat feedback and lessons as data | Fixed synthetic scope; no retrieval/model layer |
| Candidate requests broader access | Require the appropriate new decision and permission | Out-of-profile configurations blocked |
| Authority changes after approval | Check current authority at the relevant boundary | Local policy, mandate, and publication-permission cases tested; direct cross-store races remain |
| Concurrent or intervening local change | Check expected state and preserve lineage | Core SQLite generation checks; no distributed atomicity |
| Publication response is lost | Reconcile the original operation; retain unknown effect | Family lost-response and unavailable-readback cases tested |
| Historical receipt hides withdrawn resource | Inspect required current resource before activation | Withdrawn-manifest case blocks first activation |
| Crash after provider or activation commit | Recover the original durable effect or record | Selected later acknowledgement gaps tested |
| Crash during early preparation/adoption | Reconcile partial writes without duplicate decisions | Not automated; manual inspection and repair required |
| New evidence blocks activation after publication | Keep the publication visible; decide its disposition | Effect retained while activation is blocked; integrated withdrawal absent |
| Stale rollback overwrites newer work | Check authority, dependencies, and current generation | Standalone recovery tested; coordinated family recovery absent |
| Report text contains markup or instructions | Escape data; do not create executable controls | React escaping and no-script/disabled-control tests; report input is not a public API |
| Report is mistaken for live status | Label snapshot and distinguish history/current state | Static report labels; no live monitoring |
| Vendored source drifts | Pin revisions, preserve notices, inspect updates | Offline Git-blob identity check; not a supply-chain security assessment |
| Source is removed or restricted | Constrain later verification and reuse | No retention/deletion or access service |
| Development data becomes employee ranking | Separate purposes and preserve participant rights | Guidance only; no human data in fixtures |

## Before real participants or live effects

Establish the identity and data boundaries, appropriate participant involvement, trustworthy measurements, current-authority enforcement, and a provider-specific interruption/recovery design. Decide how partial writes, uncertain effects, revoked authority, and irreversible outcomes will be handled before granting live access.

The static report escapes text, but exported data can still disclose information. Minimize and authorize exports before rendering. A digest proves content identity, not truth, permission, or confidentiality.

Tests establish only their named local behaviors. Neither test volume nor documentation checks establish safety, human learning, production readiness, or full conformance.
