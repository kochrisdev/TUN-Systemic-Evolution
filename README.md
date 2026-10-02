# TUN Systemic Evolution

**Learn deliberately. Change responsibly. Evolve together.**

TUN Systemic Evolution helps people and AI systems turn experience into better judgment, better products, and better ways of working. It connects a learning question to evidence, a decision, a bounded change, and a later check that the change remains useful.

The aim is shared capability: people become better able to understand, challenge, and direct AI; AI systems become more useful through evaluated changes; organizations retain lessons without losing their context.

**Current status:** a draft framework with two runnable, synthetic local pilots and a read-only review report. The pilots test record handling and decision boundaries. They do not run or train a model, evaluate real participants, deploy a product, or demonstrate improved human learning. See [scope and non-claims](docs/SCOPE.md).

## Design · Engineer · Manage · Evolve

| Responsibility | Central question | Contribution to a learning case |
|---|---|---|
| [Design](https://github.com/kochrisdev/TUN-Systemic-Design) | Can people understand and direct the system? | Clear evidence, uncertainty, decisions, and controls |
| [Engineering](https://github.com/kochrisdev/TUN-Systemic-Engineering) | Can actions be authorized, executed, verified, and recovered? | Enforced boundaries and evidence of actual effects |
| [Management](https://github.com/kochrisdev/TUN-Systemic-Management) | What matters, who decides, and what resources may be used? | Outcomes, mandates, priorities, and accountable decisions |
| **Evolution** | What should we learn or change, and what would justify it? | Learning methods, experiments, assessed lessons, and reconsideration |

These are cooperating responsibilities, not a waterfall or four mandatory services. Evolution works throughout discovery, delivery, operation, and retirement. Management remains the owner of organizational adoption decisions; learning evidence does not grant new authority.

## A repeatable learning loop

```text
Observe → Reflect → Hypothesize → Experiment → Validate → Adopt → Monitor
   ↑                                           │                   │
   └────── revise, reject, defer, or learn ──────┴───────────────────┘
```

Not every lesson requires a release. An experiment can correct an assumption, improve human practice, support a limited adoption, or show that the baseline should stay. A useful lesson states **what we learned, from what evidence, where it applies, and what we will do differently**.

Human learning, saved context, AI configuration changes, model training, and organizational learning are distinct processes. [The concept note](docs/CONCEPT-NOTE-v0.1.md) explains the evidence each needs.

## Choose your starting point

- **Understand the idea:** [Introduction](docs/INTRODUCTION.md), [concept note](docs/CONCEPT-NOTE-v0.1.md), and [manifesto](docs/MANIFESTO-v0.1.md).
- **Use it with a team:** [First learning cycle](docs/FIRST-LEARNING-CYCLE.md), [human–AI co-evolution](docs/HUMAN-AI-COEVOLUTION-v0.1.md), and the [fictional support example](examples/human-ai-support-evolution.md).
- **Explore the implementation:** [Standalone pilot](docs/PILOT.md) or [connected family pilot](docs/FAMILY-PILOT.md).
- **Assess an adoption:** [Twelve draft requirements](docs/SPECIFICATION-v0.1.md), [partial assessment matrix](docs/CONFORMANCE-MATRIX.md), and [roadmap](docs/STATUS-AND-ROADMAP.md).

The [documentation index](docs/README.md) contains every guide, template, and validation record.

## Run the smallest demonstration

With Python 3.11 or later, from the repository root:

```powershell
python -m reference.tsev_pilot.demo
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

This standard-library pilot rejects a faster candidate that harms a synthetic human-performance measure, adopts another candidate, changes a local configuration pointer, and restores it after a simulated regression. It requires no credentials or network.

The optional [family pilot](docs/FAMILY-PILOT.md) uses pinned Management and Engineering implementations plus two actual Design components. It tests a lost publication response, keeps activation blocked while verification is unavailable, and reconciles the original operation after restart. Installing its additional dependencies requires package access; running it remains local.

## What success looks like

A team can explain what changed in its understanding, what evidence supports that change, what people practiced or learned, who decided, what actually changed in the system, and when to reconsider. Real benefit must be assessed in the intended setting. The next priority is one named, bounded learning cycle with actual participants and permitted evidence.

[Scope](docs/SCOPE.md) · [Governance](GOVERNANCE.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Licensing](vendor/README.md)

Maintained by Christopher Tun (`@kochrisdev`). Developed with AI assistance. Original repository content uses the [MIT license](LICENSE); vendored companion material retains its own notices.
