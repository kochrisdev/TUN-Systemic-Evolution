# Scope and non-claims

Updated: 2 October 2026. [Status](STATUS-AND-ROADMAP.md)

## Available

A draft discipline, manifesto, twelve requirements, human-development and operating guidance, four templates, a fictional example, two synthetic local pilots, and a read-only report.

| Part | Implemented scope | Boundary |
|---|---|---|
| Standalone Evolution pilot | Immutable-through-API configurations, experiments, observations, evaluations, decisions, local activation, monitoring, rollback | Caller-supplied synthetic evidence; local pointer only |
| Connected family pilot | Actual pinned Management review/decision, Engineering manifest publication/readback, bridge bindings, local activation | Separate trusted SQLite stores; selected interruption recovery; no distributed atomicity |
| Design report | Actual ApprovalGate and ActionReceipt, before/after snapshots, separate activation state | Static HTML, disabled decisions, no live monitor |
| Documentation checks | Relative file links, code fences, twelve requirement headings | No external-link, anchor, claim, or human-usefulness validation |
| Vendor check | Selected files match recorded upstream Git blobs after line-ending normalization | Source identity, not security or future compatibility |

The journal is not independently tamper-proof. Only the named [standalone](PILOT-VALIDATION-2026-10-02.md) and [family](FAMILY-VALIDATION-2026-10-02.md) validation scopes are supported by those runs.

## Not implemented or established

No model inference, online learning, model training, autonomous experiment execution, real metric collection, participant study, statistical causal analysis, production deployment, production authentication, tenant service, retention/deletion service, stable SDK, or hosted website is included. Prompt text is stored but never executed.

The family pilot has a simulated local provider boundary. It does not prove remote delivery behavior or complete family interoperability. Early partial writes and direct cross-store races remain limitations. Coordinated family recovery is not implemented; separate standalone recovery capabilities do not establish it.

The Evolution JSON Schema documents the experiment envelope; its runtime uses strict Python profile checks. Independent schema-engine validation of that Evolution schema and cross-language compatibility remain unassessed. The companion runtimes use their own schemas; that does not validate Evolution's schema.

Monitoring accepts manually supplied synthetic aggregate data and checks absolute operating limits. There is no scheduler, alert delivery, automatic rollback, or real outcome collector.

## Claims and versions

Use claim words with an explicit object and scope:

- **Draft-specified:** the obligation is written.
- **Implemented:** the corresponding code exists.
- **Validated:** a named check passed in a stated environment and scope.
- **Adopted:** the responsible decision was recorded.
- **Published:** the specified record was verified at its publication target.
- **Activated:** the selected configuration change was observed in its target.
- **Beneficial:** suitable outcome evidence supports that separate claim.

The document revision is v0.1. Experimental namespaces are `tsev-pilot/0.1`, `tun-family-manifest/0.1`, `tun-family-review/0.1`, and `tun-family-demo/0.1`. Cite the source commit when reviewing this evolving draft. No stable release, external certification, or full scoped conformance is claimed.

The framework does not define a universal human competence score, justify employee surveillance, or equate increased automation with progress. The next evidence must come from an appropriately scoped real learning cycle, not from relabeling synthetic checks as human results.
