# Human–AI co-evolution v0.1

Status: proposed practice. No human study has been run for this draft.

## Shared capability, distinct learning processes

Co-evolution means deliberately improving the relationship between people and AI systems. People develop judgment and skills; the AI system changes through explicit technical mechanisms; the organization improves its practices. These processes can support one another, but evidence for one does not automatically establish another.

A useful question is: **Are people becoming more capable with the system, and does that capability remain available when they need to question, correct, or work without it?** The appropriate balance depends on the task. Independent performance is essential to assess when independent competence is claimed; it is not a universal requirement that every task be done unaided.

## The human development track

| Step | Practice | Evidence to retain |
|---|---|---|
| Intention | Choose a skill or judgment that matters to the participant and workflow | Starting capability, purpose, assistance condition |
| Attempt | Work through an appropriate task and explain key choices | Reasoning and outcome, with permitted collection |
| Feedback | Compare with a rubric, expert feedback, or a checked example | What was correct, uncertain, or missed; evaluator limitations |
| Practice | Try new cases that address the observed difficulty | Changes in reasoning and recurring errors |
| Transfer | Apply the capability to unfamiliar but relevant cases | Performance with a declared assistance condition |
| Retention | Revisit comparable new tasks after a suitable interval, when relevant | What persisted and what needs renewed practice |

Let participants challenge the assessment and suggest a more useful practice task. Record the learning intervention—such as coaching or worked-example comparison—separately from the AI configuration being tested. If both change together, limit attribution to the combined intervention unless the study can separate them.

## The AI system adaptation track

Name the mechanism: a prompt revision, retrieval change, inspected memory update, tool change, model selection, workflow change, or model training. Pin artifacts and dependencies, compare representative cases, preserve regression cases, and monitor the adopted version.

Saved feedback or context is information for later use; it is not proof of model training. Training changes model parameters and requires its own data permissions, evaluation, lineage, and release process. None of these mechanisms is executed by the current pilots.

AI can propose exercises, organize permitted evidence, suggest hypotheses, and help explain results. Its suggestions remain reviewable. A candidate's favorable self-assessment cannot by itself establish that it improved.

## Assess the working relationship

| Claim | Possible observation | Limitation to preserve |
|---|---|---|
| People learned a skill | Performance on unfamiliar tasks with a declared assistance condition | Better assisted output alone does not show independent competence |
| Learning lasted | Delayed assessment on comparable new cases | Repeated exposure to the same test can inflate results |
| Reliance is better calibrated | Appropriate acceptance and rejection of correct and flawed suggestions | Fewer overrides can mean improvement or passivity |
| Review became more effective | Detection of planted defects in a controlled exercise | Planted defects may differ from real production errors |
| Work became more sustainable | Review effort, workload accounts, recovery effort | An average can hide a subgroup carrying extra work |
| People retain meaningful control | Ability to question, override, seek help, and explain responsibility | A visible button does not establish usable control under real workload |

Use only measures relevant to the decision. Include participant accounts alongside task results, and distinguish a missing observation from a poor result. For higher-consequence claims, involve suitable domain and participant reviewers. This framework supplies no universal competence score or psychological assessment.

## Participation, dignity, and data

Agree the purpose, applicable notice or consent, collection, access, withdrawal, and escalation before collecting individual observations. Explain how withdrawal affects already aggregated evidence and what cannot be withdrawn from completed actions. Prefer aggregate reporting when individual records are unnecessary.

Keep development evidence separate from employment assessment unless a distinct, transparent, authorized process establishes that purpose. Do not infer sensitive traits from interaction patterns. Do not reuse practice transcripts for training, memory, or cross-team sharing merely because they were available for feedback.

Human learning cannot be rolled back by restoring a prompt. Habits, expectations, and disclosed information may persist. If a change is withdrawn, provide explanation, coaching, and support appropriate to its residual effects.

## First field study

Choose one reversible workflow, appropriate participants, and a named owner. Establish a baseline, offer the planned practice, assess the candidate, and include transfer or retention assessment where claimed. Prespecify how experience, practice effects, case difficulty, selection, missing observations, and other simultaneous changes limit interpretation. Participant burden is part of the experiment cost.

Use the [first-cycle guide](FIRST-LEARNING-CYCLE.md) and [charter](../templates/experiment-charter.md). The pilot's `human_detection` metric is a synthetic aggregate illustrating a constraint. It is not evidence of learning, skill retention, consent, or a completed human study.
