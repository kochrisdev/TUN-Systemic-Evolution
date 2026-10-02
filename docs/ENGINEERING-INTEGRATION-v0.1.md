# Engineering integration v0.1

Status: proposed mapping; the offline pilot has no Engineering adapter.

Reviewed against [TUN Systemic Engineering at 476f649](https://github.com/kochrisdev/TUN-Systemic-Engineering/tree/476f649d41c4a0f659c15276384866908d9b9c01), particularly its scope, contracts, specification, evidence guidance, and Design mapping.

Evolution supplies exact candidate artifacts, evaluation references, proposed rollout scope, expected current state, and recovery/monitoring conditions. Engineering supplies current authorization, operations and attempts, effects, verification, intervention, and recovery. The adoption decision is an input to authority evaluation, not an execution grant.

| Evolution concept | Engineering relationship |
|---|---|
| Experiment action | New scoped `ActionProposal`, approval where applicable, authorization, and operation |
| Observation of an effect | Bound `VerificationRecord` or access-controlled evidence reference |
| Adaptation proposal | Deployment-specific `ActionProposal` with exact artifacts and preconditions |
| Adoption decision | Linked decision evidence; Engineering still evaluates current policy |
| Activation | Operation, attempts, observed effect, verification, and truthful receipt |
| Restoration | Separately authorized recovery operation linked to the original activation |

Engineering's TSE-021 already prevents memory from granting authority; TSE-030 separates product quality from execution correctness and requires relevant regression evaluation. Evolution should supply supporting evidence for those obligations.

Use an explicit adapter and record both schema and source revisions. Similar record names do not establish wire compatibility. Initial adapter acceptance should cover a stale artifact, newly contradictory evidence, revoked authority, changed active baseline, lost activation acknowledgement, unknown effect, restart, and an intervening release before rollback.

The pilot's transactional local pointer does not model a remote provider boundary. A remote host must persist intent, reconcile unknown effects, declare duplicate protection, and verify the actual deployment. Never transfer the local pilot's guarantees automatically to a provider.
