# Conformance matrix

Status: partial technical evidence only. **No complete requirement or full conformance assessment is claimed.** The [specification](SPECIFICATION-v0.1.md) remains a broader proposal. Test names below refer to [test_pilot.py](../tests/test_pilot.py), run in the [validation record](PILOT-VALIDATION-2026-10-02.md).

| Requirement | Selected executable evidence | Remaining assessment |
|---|---|---|
| TSEV-001 Purpose, scope, baseline | `test_changed_experiment_cannot_reuse_evaluation`; `test_capability_and_data_scope_expansion_are_blocked` | Named real owner, affected people, meaningful baseline and adoption boundary |
| TSEV-002 Learning claims | `test_conflicting_observations_remain_visible`; `test_unstructured_concern_blocks_adoption_even_with_passing_metrics` | Authenticated provenance, claim review, corrections, applicability and real learning |
| TSEV-003 Experiment contract | `test_profile_rejects_ambiguous_versions_fields_and_timestamps`; `test_changed_experiment_cannot_reuse_evaluation` | Assignment, sufficient sample/design, execution budgets and prespecification in real work |
| TSEV-004 Human development | `test_faster_candidate_with_human_regression_cannot_be_adopted` illustrates one synthetic constraint | Participant involvement, consent/notice, workload, agency, transfer, retention, individual access |
| TSEV-005 Data boundaries | `test_capability_and_data_scope_expansion_are_blocked` covers fixed synthetic scope only | Actual access, retention/deletion, training permission, source availability, knowledge transfer |
| TSEV-006 Bounded execution | `test_agent_cannot_approve_activate_or_restore`; `test_permission_revocation_and_renewal_invalidate_prior_decision` | Real identity, runtime budgets, external effects, containment and escalation |
| TSEV-007 Evaluation validity | `test_population_method_unit_and_window_mismatch_are_not_accepted`; `test_known_failure_is_not_hidden_by_missing_other_evidence`; `test_missing_value_and_small_sample_are_insufficient` | Real evidence, evaluator validity, contamination, uncertainty, causality, subgroup effects |
| TSEV-008 Adoption | `test_new_evidence_requires_a_new_evaluation`; `test_later_rejection_supersedes_earlier_adoption`; `test_changed_experiment_cannot_reuse_evaluation` | Authenticated Management decision, dissent, alternatives, complete scope and review triggers |
| TSEV-009 Activation | `test_supported_decision_does_not_activate_until_separate_command`; `test_concurrent_activation_commits_only_one_local_change`; `test_repeated_activation_is_blocked` | Engineering integration, dependencies, remote dispatch/readback, unknown effects |
| TSEV-010 Monitoring | `test_missing_monitoring_is_visible_and_does_not_auto_restore` and demo's synthetic breach | Actual collection, cadence, owner response, drift assessment and notifications |
| TSEV-011 Recovery/retirement | `test_rollback_cannot_overwrite_intervening_activation_even_same_artifact`; `test_rollback_requires_current_permission_and_fresh_review`; `test_restart_preserves_activation_monitoring_and_recovery_history` | Remote restoration, dependent changes, irreversible effects, retirement and residual obligations |
| TSEV-012 Assessment/method | Named report, source fingerprints, documentation checks | Human reviewer, complete applicable results, method usefulness and review burden |

For an adopter assessment, record the implementation revision, environment, exact scope, accountable reviewer, date, result for every applicable obligation, supporting evidence, open issues, justified exclusions, and recommendation departures. A selected passing test cannot discharge every clause of a requirement. Do not mark manual or integration work passed because the local example runs.
