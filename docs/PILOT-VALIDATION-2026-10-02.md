# Local pilot validation — 2 October 2026

Status: named local technical run. Assessor: Codex automated checks and source review; no independent human or external assessment. [Scope](SCOPE.md) · [Conformance mapping](CONFORMANCE-MATRIX.md)

This is the historical validation of the initial standalone pilot. The subsequent connected increment and revised documentation are assessed separately in the [family validation record](FAMILY-VALIDATION-2026-10-02.md). Original counts and fingerprints below describe that initial run, not the current whole repository.

## Environment and observed results

- Host: Microsoft Windows NT 10.0.26200.0.
- Interpreter: Python 3.13.4.
- Dependencies: Python standard library only.
- Test clock: starts at `2026-10-02T12:00:00Z`; selected tests advance it.
- Evidence: fabricated measurements, fixture actors, temporary local SQLite stores.

| Command | Observed result | Claim supported |
|---|---|---|
| `python -m unittest discover -s tests -v` | Exit 0; 27 tests passed | Selected local profile checks and state transitions |
| `python -m reference.tsev_pilot.demo` | Exit 0; expected scenario completed | Synthetic rejection/adoption, local activation, monitoring, restoration, and 25 journal records retained after reopen |
| `python scripts/check_docs.py` | Exit 0; 31 Markdown files checked | Relative file links, fenced blocks, and the twelve requirement headings |
| `python -m json.tool schemas/pilot-v0.1.schema.json` | Exit 0 | Schema document is syntactically valid JSON; not independent schema-engine validation |

The demonstration rejected a candidate whose synthetic human error-detection score declined from 85 to 70, despite faster review. A second candidate passed its synthetic criteria. An agent-fixture approval attempt was blocked; an owner-fixture decision enabled a separate local activation. A monitoring value of 70 triggered concern, and an owner-requested restoration returned the pointer to baseline. No model, human participant, customer, or provider was evaluated.

## Failure coverage

The suite exercises changed experiment/evaluation bindings; unrelated configuration evidence; missing, conflicting, non-finite, boolean, future, stale, and mismatched observations; human performance and review-time regression; material concerns outside selected metrics; expired review; new evidence after approval; agent self-approval; policy revocation and renewal; a later rejection; expanded capabilities or data scope; duplicate and concurrent local activation; missing monitoring; wrong or stale recovery evidence; an intervening activation of the same artifact; and restart history.

The concurrent test uses two independent SQLite connections and confirms one committed activation. This is evidence for the exercised local race, not a distributed exactly-once guarantee or exhaustive concurrency proof.

## Tested source identity

The initial validation was performed before the draft had a Git commit. The following SHA-256 values identify the files used in that run and can be compared with the published source. Documentation and archive packaging are outside these code fingerprints.

| File | SHA-256 |
|---|---|
| `reference/tsev_pilot/contracts.py` | `8cc6f71dd2644b7ba48fc7f132306fee2c31efcc699b9a78fbf303c0f54e4e58` |
| `reference/tsev_pilot/runtime.py` | `8c0403dee0cc6542f51e6f6e46eae0ab74dddb1aca4712c2730c6f3a07983211` |
| `reference/tsev_pilot/fixtures.py` | `fe62e1fd3676007ae73454ddd0df6e10fc2c94f3afc65de07fa639ecacf04d9c` |
| `reference/tsev_pilot/demo.py` | `5ad4d5e1bbbeb0b9b20b88e12c437778ed35b6060798f372ef2bb7322e71b4c0` |
| `tests/test_pilot.py` | `860c1950106724a33624657aee7077750da2531d0d8d66e9c839d7d027363844` |
| `schemas/pilot-v0.1.schema.json` | `50596cd69e4dbe27f84412ab831246649dd973d5aa328e4eb90e8516ff536eda` |
| `scripts/check_docs.py` | `3d2d7a610e8e940f936f932bc4299144bb7d319a0acba9f9e07b28067c245d50` |

The schema file was supplied as documentation; independent schema-engine validation was not run. The documentation checker verifies relative file links, fenced blocks, and the twelve requirement headings. It does not validate external links, anchors, human usefulness, or normative completeness.

## Limits and next evidence

The caller selects fixture roles and supplies evidence. No authentication, tenant enforcement, provenance authentication, participant protection service, live experiment, statistical causal method, production activation, remote recovery, or companion adapter is tested. Full TSEV conformance remains unassessed. The next meaningful evidence is a scoped real adoption and the first explicit Management/Engineering/Design integration.
