# Local pilot: experiment to adoption

Status: implemented experimental profile, with [named local validation](PILOT-VALIDATION-2026-10-02.md). [Scope](SCOPE.md) · [Schema](../schemas/README.md)

## Run

Requires Python 3.11 or later; the recorded run used Python 3.13.4 on Windows. From the repository root:

```powershell
python -m reference.tsev_pilot.demo
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

On systems whose Python command is `python3`, substitute that command. Only Windows was tested in this named run. The pilot has no third-party dependencies and needs no credentials or network.

By default the demo uses a temporary database removed at exit. To retain a run, choose a new file:

```powershell
python -m reference.tsev_pilot.demo --db .pilot-data/first-run.sqlite3
```

The command refuses an existing path. Runtime code uses the current UTC clock unless a fixture clock is supplied. The demo and tests use a fixed clock starting at `2026-10-02T12:00:00Z`.

## What it does

The journal stores immutable configuration and experiment records through the application API. Observations bind to an experiment, configuration, metric, population, method, unit, period, source, and observation time. The evaluator checks one aggregate per metric and configuration against the declared thresholds, case-count floor, and freshness limit.

It preserves missing and conflicting measurements. A free-text concern can block adoption even when all selected metrics pass. It does not average conflicting data or implement correction/supersession; those require a future profile.

A reviewer fixture supplies evidence and evaluations. An owner fixture can adopt, reject, or defer. Adoption captures the exact experiment, candidate, evaluation, evidence snapshot, active generation, and policy revision. Activation is a separate call that checks the latest decision, evidence, freshness, policy, and current baseline again.

Activation changes a local SQLite configuration pointer. A transaction serializes competing changes. The pointer is read back before the journal result commits. There is no prompt execution, model evaluation, or remote deployment.

Monitoring accepts synthetic values for every declared metric and checks absolute candidate limits, not the experiment's relative improvement criteria. Missing values remain `unavailable`; a breach is `concerning`. It does not schedule observations, estimate uncertainty, or act automatically.

Rollback requires an owner-fixture call, a fresh current concern or unavailable monitoring record, current policy, and the original active generation. It restores the prior pointer, records recovery, and preserves the original activation. A newer activation prevents stale restoration even if it uses the same artifact.

## Expected output

```text
All measurements below are synthetic; no model or person was evaluated.
Fast candidate: contradicted (human detection 85 -> 70).
Evidence-first candidate: supported (quality 80 -> 90; human detection 85 -> 90).
Agent self-approval: blocked.
Owner adoption: recorded; local configuration activation: verified.
Post-activation monitoring: concerning (human detection falls to 70).
Owner-requested rollback: verified
Restart: baseline restored and all 25 journal records retained.
Verified scope: local record decisions and configuration pointer only.
```

## Boundaries

Fixture names are selected by the caller, not authenticated. The process and database are trusted. Read methods have no user or tenant authorization layer. Measurements, source labels, and case counts are supplied by the caller and not independently authenticated. This is a teaching host, not a secure service.

Threshold results mean only that synthetic aggregates satisfy the declared comparison. The count of 20 is not a statistical sufficiency calculation. Human development, data permissions, experiment assignment, causal inference, evaluator quality, source authenticity, production deployment, and complete TSEV conformance remain unassessed.

The journal has no supported mutation/deletion API, retention service, database migration, or remote reconciliation. Direct database access can modify history. Repeated activation calls are rejected after the state changes; there is no distributed idempotency promise. A real integration needs the Engineering contracts for uncertain provider effects and recovery.

## Continue with the family pilot

The optional [connected demonstration](FAMILY-PILOT.md) adds actual Management and Engineering records and a Design report. Install its separate dependencies only when using that path. Its adapter recovers selected acknowledgement gaps; the standalone host described here retains its narrower behavior, including rejection of repeated activation calls.

The standalone test-discovery command above runs the core suite. Run `python -m unittest discover -s tests/family -v` separately in the optional environment to test the family bridge.
