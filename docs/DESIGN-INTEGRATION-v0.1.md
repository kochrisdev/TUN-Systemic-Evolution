# Design integration v0.1

Status: two actual Design components are used in a local, read-only report; the broader learning interface remains a proposal.

Source: [TUN Systemic Design at f1cc566](https://github.com/kochrisdev/TUN-Systemic-Design/tree/f1cc566c44a04741e51ce642ffaa0feab0bd5b36). Selected source files and notices are preserved in [vendor provenance](../vendor/README.md).

## Implemented composition

The [family pilot](FAMILY-PILOT.md) exports JSON snapshots before and after reconciliation. The renderer uses the pinned `ApprovalGate` and `ActionReceipt` components directly, with Engineering's proposal and receipt projections.

The approval gate shows the exact publication proposal and its historical approval state. Its controls are disabled: the HTML has no live decision endpoint or executable client script. The receipt concerns **publication of the adoption manifest**. A separate host section states whether Evolution recorded the local configuration change and whether that activation is still the current generation.

The before/after display preserves an unresolved publication while readback is unavailable, then shows the original operation's verified publication after restart. It does not infer activation or benefit from the receipt. Queued, blocked, and cancelled operations are not forced into receipt states the selected projection does not support.

Report text is escaped by React. The report includes no raw private source material in its synthetic fixture. A real export would still need authorization and data minimization before rendering. Escaping does not make a file safe to disclose.

## Broader design mapping

| Existing pattern | Proposed Evolution use |
|---|---|
| Intent Composer / Context Panel | State purpose, population, baseline, and permitted evidence |
| Plan View | Show experiment steps, limits, and stop conditions |
| Source View / Uncertainty Signal | Present supporting and contrary evidence with scope and limitations |
| Proposal Card / Approval Gate | Review an exact adaptation and capture its bound decision |
| Action Receipt | Show the verified effect within its actual scope |
| Memory Indicator | Explain memory reuse separately from evaluation and training |
| Human Override / Recovery Control | Request supported containment or restoration and show observed results |

Only the two components named above are implemented in this repository. Candidate additions include a baseline/candidate comparison, a learning review, and a human practice reflection. Build them when an adopter reveals a gap; no package exports are claimed for these ideas.

## Questions a learning view should answer

What changed? Why? Which evidence supported or challenged it? What did people decide? What action actually happened? What remains uncertain? When will we review it again?

Keep assessment, decision, effect, and benefit separate. Where a component cannot express a state, add a clear host explanation. Test accessibility and comprehension with intended users before treating a rendered interface as validated design.
