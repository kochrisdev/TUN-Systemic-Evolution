# Management integration v0.1

Status: an explicit adapter to the pinned Management pilot is implemented for one synthetic local case.

Source: [TUN Systemic Management at 6959643](https://github.com/kochrisdev/TUN-Systemic-Management/tree/6959643f4ab0134e20d39ae3112a38d501853d05). See [source provenance](../vendor/README.md).

## One organizational decision owner

Management owns outcomes, mandates, delegations, decisions, reviews, and `LearningRecord`. Evolution adds the experimental method and learning evidence. It must not create a competing organizational approval chain.

TSM-007 covers review and change; TSM-011 requires evidence for learning and prevents silent changes to policy or authority. Evolution makes experiment, evaluation, applicability, and follow-up links more explicit.

| Management record | Evolution contribution |
|---|---|
| Outcome / Initiative | A learning question, baseline, and decision-relevant criteria |
| Mandate / Delegation | Bounded purpose, actors, actions, data, resources, and duration |
| LearningRecord | Assessed assumption, supporting/contrary evidence, applicability, decision impact |
| Review | Findings, human effects, burden, uncertainty, and proposed next action |
| Decision | Exact adoption, rejection, deferral, policy change, or retirement |
| MetricDefinition / Observation | Versioned measurement definitions and traceable observations |

## Implemented mapping

The bridge creates a Management initiative for one supported Evolution comparison. It imports candidate observations with original source references, method, population, period, and synthetic-data limitations. Baseline values determine Management thresholds so neither the absolute operating constraint nor the required improvement is weakened:

- Higher is better: threshold = the greater of the candidate floor and baseline plus required gain.
- Lower is better: threshold = the lesser of the candidate ceiling and baseline minus required gain.

Management runs its own review over the imported observations. The fixture owner approves a mandate whose purpose binds the exact candidate and learning case. Evolution records a derived local adoption decision referencing that Management decision; the derived record exists to satisfy the local pilot's activation contract, not to assert a second organizational authority.

A separate Engineering approval and permission check governs publication. The bridge makes one USD 1.00 reservation within a USD 10.00 fixture budget. This is synthetic reservation accounting, not actual spend or a charge.

Before publication and first activation, the bridge rechecks the original evaluation against current Evolution evidence and state, the current Management mandate, decision review time, and a new Management review. A pause, superseding mandate, or conflicting evidence can block progress even after earlier approval.

## What remains proposed

The adapter does not execute a human learning program, write a general Management `LearningRecord`, measure financial value, or implement organizational governance. It imports a subset of records for one case; it is not universal schema compatibility or synchronized evidence replication.

The stores are not atomic together. Direct administrative changes may race with bridge operations, and early partial writes can require manual reconciliation. Fixture identities are caller-selected, not authenticated. Reopening a case does not renew revoked Engineering permission.

Assess whether additional learning records actually improve decisions. One application may implement all four TUN responsibilities and reuse the same organizational decision record.
