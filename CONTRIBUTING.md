# Contributing to the draft

Start with one observed need and a bounded claim. Explain the affected people, current behavior, proposed change, evidence, and limitations. Keep general specification obligations separate from the smaller pilot profile.

For behavioral changes, add a meaningful failure case and update the pilot guide and assessment mapping. For documentation changes, check local links with `python scripts/check_docs.py`. Run `python -m unittest discover -s tests -v` when modifying the pilot. Run commands from the repository root.

Do not add personal or customer data to fixtures. Examples must say whether their evidence is fictional, synthetic, or observed. Preserve historical decisions through linked records rather than rewriting their meaning. A new model, threshold, population, rubric, or permission needs an explicit version and review of the evidence it invalidates.

Use `TSEV-001` through `TSEV-012` for the current draft requirements. Use source revisions and named evidence when making validation claims. Do not present documentation checks as product validation.
