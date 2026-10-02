# Contributing

Start with one observed need and a bounded claim. Explain affected people, current behavior, proposed change, supporting and contrary evidence, and limitations. Keep broad specification obligations separate from the smaller pilot profiles.

## Documentation

Write for a reader making a decision. Define unfamiliar terms, distinguish proposal from implementation, and link to the primary explanation instead of repeating it everywhere. Mark evidence as fictional, synthetic, or observed. Preserve historical validation records; add a new record when implementation or scope changes.

Run from the repository root:

```powershell
python scripts/check_docs.py
python scripts/check_vendor.py
```

The documentation checker covers local file links, fences, and the twelve requirement headings. It does not validate external links, anchors, technical claims, or usefulness.

## Implementation

For core behavior, run:

```powershell
python -m unittest discover -s tests -v
python -m reference.tsev_pilot.demo
```

For the connected slice, install the optional dependencies and follow [the family guide](docs/FAMILY-PILOT.md). Run its separate suite and demonstration, then build/test the report:

```powershell
python -m unittest discover -s tests/family -v
python -m reference.tsev_family.demo
npm ci
npm run test:review
```

Add a meaningful failure case for changed behavior. Keep source pins, vendor manifest, tests, status, and assessment mapping consistent. Do not modify vendored components silently; put adapter behavior outside the snapshot or explicitly review and document an upstream revision update.

## Evidence and responsibility

Do not add personal or customer data to fixtures. New models, thresholds, populations, rubrics, or permissions need explicit versions and a review of invalidated evidence. Preserve decisions through linked records rather than rewriting history.

Use `TSEV-001` through `TSEV-012` for the current requirements. Name source revisions, commands, environment, scope, and limitations for validation claims. A passing technical test does not establish human learning or organizational value. See [governance](GOVERNANCE.md) and [licensing/provenance](vendor/README.md).
