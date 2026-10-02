# Family increment validation — 2 October 2026

Status: named local technical checks. Assessor: Codex automated checks and source review; no independent human or external assessment.

This record covers the connected family increment and accompanying documentation refresh. The [initial standalone validation](PILOT-VALIDATION-2026-10-02.md) remains a historical record. Neither record establishes full TSEV conformance or human learning.

## Environment

- Host: Microsoft Windows NT 10.0.26200.0.
- Python: 3.13.4 in an isolated environment.
- Node.js: 22.23.2; npm: 10.9.8.
- Python dependency versions: [requirements-family.txt](../requirements-family.txt).
- JavaScript dependency graph: [package-lock.json](../package-lock.json); React 19.2.0 and TypeScript 5.8.3.
- Companion source: the three full commit pins and 20 upstream file identities in [vendor/manifest.json](../vendor/manifest.json).
- Evidence: synthetic aggregates, caller-selected fixture identities, temporary local SQLite stores, fixed clock starting at `2026-10-02T12:00:00Z`.

Dependency installation used package registries. The pilots themselves did not call a model, cloud provider, or remote deployment target. Commands below used the isolated Python interpreter where optional dependencies were needed.

## Observed results

| Check | Observed result | Supported claim |
|---|---|---|
| `python -B -m unittest discover -s tests -v` | 27 passed | Standalone core behaviors still pass |
| `python -B -m reference.tsev_pilot.demo` | Exit 0; 25 records retained after reopen | Original synthetic activation/monitoring/rollback scenario |
| `python -B -m unittest discover -s tests/family -v` | 16 passed | Selected adapter bindings, authority checks, uncertain effects, and interruption recovery |
| `python -B -m reference.tsev_family.demo --report ...` | Exit 0; paired JSON snapshots created | Baseline retained during unavailable readback; original publication reconciled; one effect and one reservation; one local activation |
| `npm run test:review` | TypeScript build succeeded; 4 passed | Actual selected Design components render; text escaped; decisions disabled; publication and activation remain separate |
| `npm run review:render -- input.json output.html` | Exit 0; static HTML created | Demo JSON can be rendered by the tested renderer |
| `python scripts/check_vendor.py` | 20 files matched | Selected source matches recorded upstream Git blobs after CRLF normalization |
| `python -m json.tool schemas/pilot-v0.1.schema.json` | Exit 0 | Evolution schema is syntactically valid JSON, not schema-engine conformance |
| `python scripts/check_docs.py` | Exit 0; 35 Markdown files and 12 requirement headings checked | Local file links, fences, and requirement inventory only |

The family scenario recorded one USD 1.00 fixture reservation within a USD 10.00 budget. It did not charge or spend money. The Engineering receipt verified manifest publication; the Evolution activation record separately established the local pointer change.

## Exercised failure cases

The family suite covers candidate/evaluation/decision bindings; preservation of baseline-relative thresholds; native reference-version types; blocked agent adoption; changed evidence before adoption; stale publication approval; a paused or superseded Management mandate; revoked Engineering publication permission; lost publication response and unavailable readback; original-operation recovery after reopen; interruption after provider commit; interruption after Evolution commit but before bridge acknowledgement; adverse evidence after publication; a withdrawn resource despite a historical successful receipt; reconciliation after pause without first activation; and prevention of a replacement case for an unresolved operation.

Renderer checks cover selected actual component states, disabled controls and absence of executable script, escaped untrusted text, mismatched/unsupported report versions, and refusal to treat publication alone as established local activation. The report is a trusted local demonstration format, not a validated public input API.

## Tested source identity

These SHA-256 fingerprints cover the increment's principal source, dependency, test, and checking files, with CRLF normalized to LF. They are recorded before the publication commit; source history identifies the surrounding repository revision. Original core source is unchanged from the initial publication.

| File | SHA-256 of normalized UTF-8 source |
|---|---|
| `reference/tsev_family/bridge.py` | `acf4e0baa297e634bb2add5d20596a05371cce1bc01065cfca03bb855b8af6b7` |
| `reference/tsev_family/demo.py` | `51163778df1d711c708a273410256eab149abd12694d6f01cb4b124010356179` |
| `tests/family/test_family.py` | `d76e9dc307b604b0eae39dff4baca9cb25080f9fb87e8712fa13d6bb9ff4f5e9` |
| `review/src/Review.tsx` | `4d50360d59daf555451217e304e6d0a7e7671d4c7783e34d4b8d678e45b4d62b` |
| `review/render.mjs` | `ee8c7f6e7cf1722364aee2c9e8b8a6d3db8a347f5f4541db10407c332e57c2ae` |
| `review/render.test.mjs` | `1236a512cb020ae8f6e6490eaef1b9d0f317abdb72782911cc6c2914b08dbf78` |
| `review/layout.css` | `0990932872705dfe125e452036cefd6dc8631a72db0f94b408e7c4d8c1131fb6` |
| `package-lock.json` | `04e2d945c5c45b3cbc4a8d905b622830a6ed686780e53a8e1d9cb8401663cf06` |
| `requirements-family.txt` | `ab5f7e6a803e7140ea63bf8960b6e90a1b4e7db5aefb4bdee2af925e66189f16` |
| `scripts/check_docs.py` | `9417427ccd655bfc11201ed57d0519c5a6196d99d9b4b3fbe50b8ff09a8173a6` |
| `scripts/check_vendor.py` | `3fdc3257e0920e3ace8ed4c602f6af663f1dfcf339f84ee0fbae03a0b80eeb77` |
| `vendor/manifest.json` | `204b5ce8d9c75d88e6b395f6af8a602ca2bc84b7178c5a5cd7863358f9ea5604` |

The vendor manifest supplies separate upstream Git blob identities. A hash identifies content; it does not authenticate measurements, certify security, or establish a claim's truth.

## Final verification and limitations

The documentation checker passed for 35 Markdown files, and the tracked-change whitespace check passed. This record does not claim browser visual review: the app's browser policy blocked opening the local HTML file. Automated rendering passed; responsive appearance, accessibility, and user comprehension remain unassessed.

The stores are not atomic together. Independent direct mutations can race with bridge checks. Early preparation/adoption interruptions can leave partial records needing manual reconciliation. Coordinated family withdrawal/rollback, real identity and evidence, live deployment, data lifecycle controls, participant safeguards in software, and real human outcomes remain unimplemented or unassessed.

For the relationship between tests and broader obligations, see the [partial conformance matrix](CONFORMANCE-MATRIX.md). The next useful evidence is a named real learning cycle and the controls required by that context.
