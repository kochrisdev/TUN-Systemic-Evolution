# Connected family pilot

Status: experimental, synthetic, and local. [Validation record](FAMILY-VALIDATION-2026-10-02.md) · [Threat model](THREAT-MODEL.md) · [Source provenance](../vendor/README.md)

This pilot connects actual pinned companion implementations around one narrow question: can an approved learning case produce a verified publication and then a separate local configuration change, while preserving unresolved effects and decision boundaries?

## What connects

```text
Evolution evidence → Management review and exact mandate decision
                               ↓
                    Derived local adoption record
                               ↓
           Engineering proposal → approval → publication
                               ↓
                   Reconcile and verify original effect
                               ↓
             Recheck current conditions → local activation
                               ↓
               Design components → read-only HTML report
```

The published object is an adoption manifest containing the candidate digest, experiment/evaluation/evidence bindings, Management decision and mandate, and source revisions. Publication does not deploy a model. Evolution activation changes only the original pilot's local pointer.

## Run the connected demonstration

Use Python 3.11 or later. From the repository root, create an optional environment; these commands are for Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-family.txt
.venv\Scripts\python.exe -B -m unittest discover -s tests/family -v
.venv\Scripts\python.exe -B -m reference.tsev_family.demo --report .pilot-data/family-review.json
```

On other systems, use the corresponding virtual-environment interpreter path. The recorded run was on Windows; portability to other hosts is not established by that run.

The core pilot remains standard-library only. The family pilot adds the pinned JSON Schema dependency stack used by the companion hosts. Dependency installation needs package access; the demonstration makes no remote service calls.

The demo uses temporary stores by default. To retain them, add `--directory .pilot-data/family-run`. Both the directory and report file must be new; existing paths are refused. Select new names for another run.

## Expected scenario

1. Evolution receives the same supported synthetic comparison as the standalone example.
2. Management reviews imported observations, approves the exact mandate, and reserves USD 1.00 within a USD 10.00 fixture budget. No money is spent.
3. Engineering publishes the manifest, but the demonstration discards the response.
4. Provider readback becomes unavailable. Activation is refused and the baseline remains active.
5. After reopening the stores, reconciliation verifies the original publication.
6. Evolution activates the exact candidate locally after current checks.
7. A repeated activation request returns the original activation record without changing the pointer again.

The scenario verifies one provider effect and one Management reservation. Fixture clocks begin at `2026-10-02T12:00:00Z`; observations and expiry conditions are fixed for repeatable tests. UUIDs vary across runs.

## Render the read-only Design report

With Node.js and npm available, after generating the JSON:

```powershell
npm ci
npm run test:review
npm run review:render -- .pilot-data/family-review.json .pilot-data/family-review.html
```

The test command builds the TypeScript renderer. If rendering without tests, first run `npm run review:build`. The output HTML path must be new. Open it in a browser; no server is required.

The report uses actual pinned `ApprovalGate` and `ActionReceipt` components. It displays historical states with disabled decisions and no client-side script. The input is the demo's trusted local report format, not a public ingestion API: version/case checks and text escaping are not comprehensive arbitrary-input validation or evidence authentication.

## Stores and recovery

Five SQLite files keep responsibilities explicit: Evolution journal/state, Management records, Engineering operations, provider resources, and bridge case/event links. The bridge imports the Management decision into the local Evolution contract; it does not create an independent organizational decision owner.

The bridge serializes its own writes but cannot atomically commit all stores. Tested recovery covers lost publication response, interruption after provider commit, and interruption after Evolution commits before bridge acknowledgement. Reconciliation reads original effects even after a mandate pause; a pause still prevents first activation.

Early interruption during case preparation or adoption can leave partial companion records that require manual inspection and reconciliation. Do not infer an all-stage crash-recovery guarantee. A published manifest may remain after new evidence blocks activation. Returning a previous activation record is a historical acknowledgement, not a new action or proof it is still current; consult the report's current state.

## Deliberate limits

- Identities, measurements, clock, process, and database access are trusted fixtures.
- There is no model call, real participant, deployment service, or authenticated source collection.
- Direct changes outside the bridge can race between checks and effects.
- Engineering verifies manifest publication; Evolution verifies its local pointer under its own fixture policy.
- Integrated withdrawal/rollback, reservation settlement, retention/deletion, and distributed transactions are not implemented.
- Standalone recovery examples remain separate; this demonstration does not run coordinated family recovery.
- The report is a snapshot, not a live monitor or an authorization interface.

For implementation details, see the [Management](MANAGEMENT-INTEGRATION-v0.1.md), [Engineering](ENGINEERING-INTEGRATION-v0.1.md), and [Design](DESIGN-INTEGRATION-v0.1.md) guides. None of this establishes full TSEV conformance or human learning.
