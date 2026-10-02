# Threat model for the draft and pilot

Status: initial threat inventory, not a security assessment.

The local pilot trusts its Python process, caller-selected fixture identities, filesystem, clock, and SQLite store. It accepts synthetic or caller-supplied measurements. It has no network boundary, identity provider, encryption, tenant isolation, provider, model, or independent evidence authentication. Application checks do not protect against a caller editing the database or impersonating a fixture owner.

| Failure or threat | Required response in an adopting system | Current pilot evidence or gap |
|---|---|---|
| A candidate grades itself favorably | Identify evaluator limitations; use appropriate independent evidence | Source/limitations recorded; no evaluator executed |
| Test contamination or repeated tuning | Pin cases; separate tuning and assessment; disclose selection | Method references only; manual assessment remains |
| Faster work reduces human error detection | Preserve human constraints separately from speed | Synthetic candidate rejected in a named test |
| Averages hide adverse effects | Assess affected groups and retain participant concerns | Explicit concern blocks adoption; no subgroup analysis |
| Conflicting, missing, or stale evidence | Preserve and constrain the conclusion | Conflicts, missingness, bindings, count, and age checked |
| New evidence appears after approval | Reassess before activation | Evidence snapshot checked at activation |
| Feedback injects instructions or permissions | Treat feedback as data and enforce current authority | Fixed capabilities and data scope; no retrieval/model layer |
| Candidate requests broader tools or data | Return to Management and Engineering authorization | Out-of-profile configurations blocked from experiments |
| Owner permission is revoked | Block activation; obtain a fresh applicable decision | Policy revision and enabled state checked |
| Concurrent changes race | Compare current state and preserve lineage | SQLite write transaction and generation checks |
| A stale rollback overwrites newer work | Check current generation and dependencies | Local generation checked, including same-artifact reactivation |
| Remote activation response is lost | Reconcile the original operation; retain unknown effect | No remote provider; local success cannot cover this threat |
| A source is removed or restricted | Update evidence availability and claim limits | No retention/deletion or access service implemented |
| Employee development data becomes ranking | Separate purposes and preserve participation rights | Documentation only; no human data in fixtures |

Prioritize a real identity boundary, authenticated evidence, a bounded provider integration, and participant review before introducing live actions or personal information. The documentation checker and local tests cannot establish those properties.
