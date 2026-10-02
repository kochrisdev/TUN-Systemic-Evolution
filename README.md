# TUN Systemic Evolution

**Learn deliberately. Change responsibly. Evolve together.**

TUN Systemic Evolution is a proposed discipline for helping people, AI systems, and organizations improve through evidence, practice, bounded experiments, and accountable change. It connects a lesson to the exact change it supports, the decision to adopt that change, and what happens afterward.

**Status: draft specification with an experimental offline pilot.** The pilot exercises decisions against synthetic measurements and changes a local configuration pointer. It does not run a model, train one, deploy a product, or establish human learning or organizational benefit. Companion integrations are proposed mappings.

## One family, four responsibilities

| Project | Central question |
|---|---|
| [TUN Systemic Design](https://github.com/kochrisdev/TUN-Systemic-Design) | How do people understand and control AI behavior? |
| [TUN Systemic Engineering](https://github.com/kochrisdev/TUN-Systemic-Engineering) | How are actions authorized, executed, verified, and recovered? |
| [TUN Systemic Management](https://github.com/kochrisdev/TUN-Systemic-Management) | How do organizations choose outcomes, delegate authority, allocate resources, and adapt? |
| **TUN Systemic Evolution** | How do people and AI turn experience into supported learning and sustained improvement? |

Evolution operates throughout design, engineering, and management. The four are cooperating responsibilities, not a waterfall or four required services. Management retains ownership of priorities, policy, mandates, and adoption decisions. Evolution supplies the learning method and evidence for those decisions.

## The working loop

```text
OBSERVE → REFLECT → HYPOTHESIZE → EXPERIMENT → VALIDATE → ADOPT → MONITOR
   ↑                                                             │
   └─────────────────────────────────────────────────────────────┘
```

At validation, a team may revise, reject, or defer. A failed hypothesis can produce valuable learning. Adoption requires a separate decision; stronger performance does not grant additional authority.

Human learning, AI configuration changes, persistent memory, and model training are different processes. Each needs its own evidence and data-use boundaries. [The concept note](docs/CONCEPT-NOTE-v0.1.md) explains the distinction.

## Start here

- [Introduction](docs/INTRODUCTION.md): the idea through a support-team example.
- [Concept note](docs/CONCEPT-NOTE-v0.1.md): purpose, boundaries, differentiators, and development approach.
- [Manifesto](docs/MANIFESTO-v0.1.md): twelve commitments.
- [Proposed specification](docs/SPECIFICATION-v0.1.md): twelve assessable requirements, using the `TSEV` prefix to distinguish Engineering's `TSE` requirements.
- [Human–AI co-evolution](docs/HUMAN-AI-COEVOLUTION-v0.1.md): learning and judgment on both sides of the relationship.
- [Worked example](examples/human-ai-support-evolution.md): a fictional experiment and a rejected faster candidate.
- [Local pilot](docs/PILOT.md): run the narrow implementation.
- [Documentation index](docs/README.md): all guides, templates, and evidence.

## Run the offline demonstration

With Python 3.11 or later, from this folder:

```powershell
python -m reference.tsev_pilot.demo
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

The pilot uses Python's standard library. It creates a temporary SQLite database, checks synthetic evidence, records an adoption decision, activates one local configuration, observes a synthetic regression, restores the prior pointer, and verifies persistence after reopening. No network or credentials are needed.

## First useful outcome

A team can explain what it learned, what evidence supports that learning, what changed, who decided, what remains uncertain, and when to reconsider. The next milestone is one real, bounded adoption with a named product and participants; see the [roadmap](docs/STATUS-AND-ROADMAP.md).

[Scope](docs/SCOPE.md) · [Governance](GOVERNANCE.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [MIT license](LICENSE)

Maintained by Christopher Tun (`@kochrisdev`). This initial draft and reference pilot were developed with AI assistance.
