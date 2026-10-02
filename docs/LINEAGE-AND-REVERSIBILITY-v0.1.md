# Lineage and reversibility v0.1

Status: proposed guidance.

Trace the signal and hypothesis through the experiment, observations, evaluation, adoption decision, Engineering operation, activation evidence, monitoring, and any recovery. Use immutable versions for material meaning. Store only the source material needed and permitted; link protected content where copying would expand exposure.

Pin models where the provider supports it, prompts, tools, retrieval settings, data/evaluation manifests, adapters, policies, and relevant environment versions. Where a provider cannot reproduce a model revision, record that limitation rather than claiming exact replay.

Before adoption, name a supported recovery target and its prerequisites. Restoring an earlier artifact can be unsafe after a schema migration, dependency change, credential revocation, or an intervening release. Check current compatibility, authority, and state at recovery time. A rollback request is not evidence of restoration.

Preserve the original activation and all effects. Restoring a prompt does not recall sent messages, delete copies, undo learning by people, or reverse transactions. Where full restoration is unavailable, describe correction, compensation, containment, or escalation accurately.

The offline pilot stores immutable records through its application API and a separate active-configuration pointer with a generation counter. Activation and rollback use transactional state checks, preserve the journal, and read back the local pointer. This establishes local pointer behavior only; it is not remote recovery, cryptographic integrity, or protection against a database administrator.

The connected family pilot adds links across Management decisions, Engineering publication operations, provider resources, and local Evolution activation. It recovers the original operation or activation in specifically tested acknowledgement gaps. Those are recovery of knowledge about an effect, not reversal of the effect.

Coordinated manifest withdrawal and configuration rollback are not implemented. A publication may survive a blocked activation, and human learning may survive a reverted configuration. Keep these residual states visible and obtain the relevant recovery decision instead of describing the whole case as “undone.”
