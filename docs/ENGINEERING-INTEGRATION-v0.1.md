# Engineering integration v0.1

Status: a narrow local publication adapter is implemented. Production deployment and integrated recovery are not.

Source: [TUN Systemic Engineering at 476f649](https://github.com/kochrisdev/TUN-Systemic-Engineering/tree/476f649d41c4a0f659c15276384866908d9b9c01). The [vendored snapshot](../vendor/README.md) includes the actual host, SQLite provider, contracts, schemas, and presentation mapping used by the bridge.

## Responsibility boundary

Evolution supplies the exact candidate, evaluation, evidence binding, expected baseline, and proposed adoption scope. Management supplies the organizational decision. Engineering independently checks the authority for an effect and retains its operation, attempts, verification, and recovery history. A favorable evaluation or available Management budget is not Engineering execution authority.

Engineering's TSE-021 separates memory from authority; TSE-030 separates product quality from execution correctness. Evolution supplies related learning evidence without replacing those responsibilities.

## Implemented path

1. A Management-approved, candidate-specific case produces a versioned adoption manifest.
2. The Engineering host creates a proposal to publish that exact manifest to the local `evolution-adoption-catalog` target.
3. A separate fixture-owner approval binds the exact Engineering proposal version. The bridge records its operation before dispatch.
4. Engineering enforces its publication permission and dispatch budget, then writes to its separate SQLite provider.
5. Reconciliation checks the original operation. A lost response remains unresolved until readback establishes its effect.
6. Before a first local activation, the bridge checks current Evolution evidence/state and Management authority, a verified publication receipt, and the current provider resource's exact content, target, revision, and non-withdrawn state.
7. Evolution performs its own transactional local pointer activation under its fixture policy.

The Engineering receipt verifies **manifest publication**, not the Evolution pointer change. Engineering publication permission is not a general deployment permission; the pointer is still governed by Evolution's local fixture controls. No live model or deployment provider is connected.

Management references retain integer versions; Engineering proposal references retain string versions. The adapter preserves both instead of assuming similarly named records share a wire format.

## Failure and recovery boundaries

Tests exercise stale proposal approval, revoked Engineering publication permission, changed Management authority, changed learning evidence, lost responses, unavailable readback, provider-commit interruption, restart, withdrawn current publication, and an interruption after Evolution commits but before the bridge records acknowledgement.

The stores do not share an atomic transaction. The bridge serializes its own calls; independent direct changes can race between its checks and effects. Early setup or adoption interruptions can leave companion records requiring manual reconciliation. The tested later recovery paths do not establish recovery from every interruption.

The provider is local and simulated; network delivery, production identity, external deployment, and distributed exactly-once behavior are not demonstrated. Standalone Engineering withdrawal and standalone Evolution rollback remain separate. A coordinated family recovery needs an explicit authorized workflow, current preconditions, verification, and an account of remaining effects.

See [family operation guide](FAMILY-PILOT.md) and [validation scope](FAMILY-VALIDATION-2026-10-02.md).
