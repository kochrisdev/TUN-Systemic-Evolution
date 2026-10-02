# Design integration v0.1

Status: proposed mapping; no React adapter or interface is implemented here.

Reviewed against [TUN Systemic Design at f1cc566](https://github.com/kochrisdev/TUN-Systemic-Design/tree/f1cc566c44a04741e51ce642ffaa0feab0bd5b36), including its README, scope, status, and the Engineering companion's pinned presentation mapping. No new inspection of every component API is claimed.

| Existing pattern | Proposed Evolution use |
|---|---|
| Intent Composer / Context Panel | State learning purpose, population, baseline, and permitted evidence |
| Plan View | Show experiment steps, limits, and stop conditions |
| Source View / Uncertainty Signal | Present supporting and contrary evidence with scope and limitations |
| Proposal Card / Approval Gate | Review an exact adaptation and capture its bound decision |
| Action Receipt | Show an Engineering-verified activation, not a claim of improved outcomes |
| Memory Indicator | Explain actual memory reuse separately from evaluation and training policy |
| Human Override / Recovery Control | Request supported containment or restoration and show observed results |

Candidate new patterns are a baseline/candidate comparison, a learning review, and a human practice reflection. Build them only after an adopter demonstrates a gap in the existing composition. Do not invent package exports for these ideas.

The learning view should answer: What changed? Why? What evidence helped and contradicted it? What did people decide? Has it activated? What remains uncertain? When will we review it again?

Preserve separate assessment and action states. `supported` evidence is not a completed deployment; a completed deployment is not verified benefit. If a component cannot represent a state, add a host view that states it explicitly. Filter private evidence before sending it to the client, and test accessibility and comprehension with the intended users.
