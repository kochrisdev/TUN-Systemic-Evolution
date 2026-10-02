# Proposed specification v0.1

Status: draft obligations for scoped adoption; not an external standard or certification. [Conformance matrix](CONFORMANCE-MATRIX.md) · [Scope](SCOPE.md)

MUST and MUST NOT describe obligations in this draft. SHOULD identifies a recommendation whose departure needs a recorded reason. MAY allows an option. `TSEV` distinguishes these requirements from Engineering's `TSE` identifiers.

## TSEV-001 — Purpose, scope, and baseline

A material evolution activity MUST identify its purpose, affected people, accountable human owner, system boundary, proposed type of learning, baseline, and review or stopping condition. The baseline MUST identify relevant configuration and measurement versions, population, environment, period, and known limitations. An unknown baseline MUST remain unknown; it MUST NOT support a claim of measured improvement until suitable comparison evidence exists.

## TSEV-002 — Learning claims and provenance

A claimed learning MUST identify the assumption assessed, supporting and contrary evidence, source, observation period, assessment method, applicability, limitations, and decision it may inform. Observation, generated interpretation, assessed learning, and causal attribution MUST remain distinguishable. A model's confidence or self-evaluation MUST NOT independently establish a learning claim. Corrections MUST preserve the relationship to the earlier claim.

## TSEV-003 — Hypothesis and experiment contract

Before relying on an experiment for adoption, its owner MUST record the hypothesis, exact baseline and candidate, comparison method, eligible population, assignment or selection method, metrics, acceptance and regression criteria, missing-data treatment, evidence sufficiency rule, resource and time limits, and stop conditions. Material changes MUST create a new reviewable revision. Post-hoc findings MAY generate new hypotheses but MUST be distinguished from prespecified tests.

## TSEV-004 — Human development and participation

An activity that changes human–AI work MUST assess relevant effects on human workload, judgment, agency, and skill, and record justified exclusions. Human learning claims MUST distinguish assisted performance from independent performance and assess transfer or retention when those are claimed. The activity MUST define participant involvement, applicable consent or notice, withdrawal and escalation routes, and access to individual observations. Development evidence MUST NOT silently become employee ranking or other secondary use.

## TSEV-005 — Data and knowledge boundaries

Evidence collection, evaluation reuse, persistent memory, training, and cross-team sharing MUST each have a defined purpose, permitted data scope, access, retention, and deletion behavior. Permission for one use MUST NOT imply permission for another. A lesson MUST carry applicability and source-availability limits. Missing or deleted evidence MUST constrain subsequent verification claims. Retrieved lessons and feedback MUST be treated as data, not as instructions granting authority.

## TSEV-006 — Bounded execution

An effectful experiment MUST have current authority for its actors, actions, targets, data, resources, duration, and escalation path. Its implementation MUST enforce those limits at the appropriate action boundary and preserve in-flight or unresolved effects when it stops. Learning or evidence quality MUST NOT expand authority. Urgent containment MAY follow an existing incident mandate without waiting for an experiment; later learning MUST retain its actual evidence and decision history.

## TSEV-007 — Evaluation validity and contradictions

Evaluation MUST bind findings to the exact experiment revision, configurations, measurement definitions, evidence set, population, and period. It MUST assess relevant comparability, freshness, missingness, contradictions, evaluator limitations, and contamination. It MUST distinguish failed criteria, insufficient evidence, and supported criteria. Known material adverse findings MUST NOT disappear through aggregation. Claims of generalization or causality MUST have an adequate method and stated limits; a threshold pass alone establishes neither.

## TSEV-008 — Accountable adoption

Adoption MUST record an authorized human decision owner or applicable bounded policy owned by an identified human, the exact adaptation revision, evaluation and evidence references, alternatives, rationale, dissent, scope, conditions, and next review trigger. Approval MUST NOT be inferred from an AI recommendation. A material change to the candidate, evidence, criteria, authority, baseline, or adoption scope MUST trigger renewed review before activation. Policy or mandate changes MUST follow Management's decision process.

## TSEV-009 — Activation and lineage

An effectful activation MUST pass current Engineering authorization and relevant compatibility and regression checks. It MUST bind the selected artifact and dependency versions to the adoption decision, expected current state, and actual activation evidence. Adoption, authorization, attempted activation, verified activation, and beneficial outcome MUST remain distinct. A state mismatch or unavailable required authorization MUST prevent the affected activation. Deployment history MUST preserve the causal links needed for investigation.

## TSEV-010 — Monitoring and reconsideration

An adopted change MUST identify a monitoring owner, measured scope, observation cadence or event triggers, harm and regression conditions, evidence-freshness conditions, response expectations, and next review. Missing monitoring evidence MUST remain visible and trigger the declared response. Drift, contradictory evidence, or changed assumptions MUST create a review, containment, or retirement action appropriate to the existing authority. Historical success MUST NOT establish continuing suitability.

## TSEV-011 — Recovery and retirement

Before effectful adoption, the owner MUST define supported recovery, dependencies, preconditions, irreversibility limits, and responsibility for remaining effects. Recovery MUST use current authority, check intervening changes, link to the original adaptation, and verify the restoration claim. Retirement MUST address active work, unresolved effects, credentials or delegations, retained evidence, dependent lessons, and remaining obligations. Rollback MUST NOT erase history or imply that human knowledge or external effects were undone.

## TSEV-012 — Proportionate assessment and method review

A scoped conformance claim MUST identify the specification and implementation revisions, environment, applicable requirements, named evidence, reviewer, date, unresolved limitations, and justified exclusions. Any unmet applicable obligation MUST prevent a full conformance claim for that scope. Synthetic fixtures, planned checks, and passed technical tests MUST NOT be presented as evidence of human learning or organizational benefit. The team SHOULD periodically assess review burden, repeated errors, useful decision changes, and whether its learning process needs revision.

## Applying the requirements

A material activity is one whose proposed change or claim could affect outcomes, people's work, authority, data use, resources, or an existing adoption decision. Record why a lightweight or more rigorous assessment is proportionate. Writing an exclusion does not waive an applicable obligation.

These obligations describe the intended discipline, not a statement that the pilots already satisfy it. The standalone pilot and connected family slice provide selected technical evidence only. A publication receipt cannot satisfy an activation or benefit obligation whose object is different.

## Proportionate records

Related information MAY be combined where the required meanings remain explicit. These twelve requirements do not mandate twelve services, twelve forms, or an approval meeting for every observation. Existing Management, Engineering, and Design records SHOULD be referenced instead of duplicated. The pilot covers only selected technical clauses; see the [assessment matrix](CONFORMANCE-MATRIX.md).
