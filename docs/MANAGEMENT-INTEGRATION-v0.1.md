# Management integration v0.1

Status: proposed mapping; the offline pilot does not read or write the Management pilot.

Reviewed against [TUN Systemic Management at 6959643](https://github.com/kochrisdev/TUN-Systemic-Management/tree/6959643f4ab0134e20d39ae3112a38d501853d05), including its specification, records, reviews, human accountability, and measurement guidance.

Management already owns outcomes, mandates, delegations, decisions, reviews, and `LearningRecord`. Evolution elaborates the method and evidence for learning. Keep Management as the source of organizational decisions and avoid a second competing approval chain.

| Management record | Evolution contribution |
|---|---|
| Outcome / Initiative | A scoped learning question and baseline relevant to the outcome |
| Mandate / Delegation | Experiment purpose, actors, actions, data, budgets, duration, stop and escalation conditions |
| LearningRecord | Assessed assumption, experiment/evidence references, contrary findings, applicability, decision impact |
| Review | Evaluation, human effects, total cost, uncertainty, and proposed next action |
| Decision | Bound adoption, rejection, deferral, policy change, or retirement |
| MetricDefinition / Observation | Versioned measurement definitions and traceable scoped observations |

TSM-007 already covers review and change. TSM-011 already requires evidence for learning and forbids silently changing policy or authority. Evolution makes the experiment, evaluation, transfer, and post-adoption links more explicit without taking those decisions away from Management.

An integration should bind the initiative and current mandate revision to the experiment, and bind the adoption decision to the exact adaptation and evaluation. If an experiment needs more data access or resources, obtain an authorized change and new review. An available budget is not execution authority.

Assess whether the extra learning records improve actual decisions and whether their maintenance cost is reasonable. A useful integration may store all four TUN responsibilities in one application and reuse the same decision record.
