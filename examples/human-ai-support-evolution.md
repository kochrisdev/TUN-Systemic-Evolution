# Worked example: support drafting

**All people, measurements, thresholds, and outcomes in this example are fictional.** The local demonstration uses matching synthetic aggregates. These are teaching values, not recommended targets or experiment results.

## The question

A team uses an AI to draft support replies; a person reviews and sends them. Reviewers find that concise drafts are quicker to inspect but sometimes omit the basis for an answer. The team asks whether showing the evidence and uncertainty can improve draft quality while preserving reviewer judgment and effort.

Management keeps the initiative limited to drafting. Sending permission stays with the person. The candidate changes a prompt; it does not add tools, persistent memory, training, or customer-data access.

## The comparison

The fictional baseline and two candidates are assigned these aggregates:

| Measure | Baseline | Fast candidate | Evidence-first candidate | Prespecified illustrative criterion |
|---|---:|---:|---:|---|
| Draft quality (%) | 80 | 90 | 90 | At least 85 and at least 5 percentage points above baseline |
| Reviewer defect detection (%) | 85 | 70 | 90 | At least 80 and no decline from baseline |
| Review minutes per case | 5 | 3 | 4.5 | At most 6 and no increase from baseline |

The offline fixture declares 20 cases per measurement. This is only a completeness guard. There are no underlying sampled replies or people, no statistical uncertainty calculation, and no real comparison study.

## Review and decision

The fast candidate fails the human detection criterion. Its speed does not cancel that failure. The evidence-first candidate passes the three synthetic checks. A reviewer can prepare that finding; an agent cannot approve its own adoption in the fixture policy.

The owner records adoption of the exact candidate and experiment, then separately activates it in the local configuration store. No message is sent and no model is called. A real adoption would require actual comparable observations, participant involvement, current authority, and appropriate evaluation before deployment.

## Monitoring and recovery

The demonstration supplies a new synthetic human-detection value of 70, below the operating floor of 80. Monitoring becomes `concerning`; it does not itself roll back. The owner requests restoration. The host checks current permission and the active generation, restores the baseline pointer, and preserves the original decision, activation, monitoring, and recovery records. Reopening the store preserves all 25 records.

This demonstrates a record and decision workflow. It cannot establish whether the prompt improves quality, whether participants learned, or whether a customer benefited.

## The real human learning question

For a future field study, let reviewers articulate their reasons, receive feedback, practice on new cases, and complete a delayed transfer task with a stated assistance condition. Check error detection, appropriate reliance, review burden, and participant feedback. Use different case sets or an appropriate comparison design to address practice and contamination. Human capability should be measured separately from assisted task performance.

## Connections across TUN

Design presents the exact change, evidence, uncertainty, and controls. Engineering authorizes and verifies a real deployment and any recovery. Management owns the experiment resources and adoption decision. Evolution preserves the tested assumption, method, findings, applicability, and monitoring conditions.
