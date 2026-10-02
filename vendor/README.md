# Companion source provenance

The family pilot uses selected, unmodified source files from these pinned repositories. This is a small vendored snapshot, not a package release or a claim of compatibility with future upstream revisions.

| Component | Source revision | Selected material | Preserved notice |
|---|---|---|---|
| Design | [f1cc566](https://github.com/kochrisdev/TUN-Systemic-Design/tree/f1cc566c44a04741e51ce642ffaa0feab0bd5b36) | ApprovalGate, ActionReceipt, supporting types and styles | [CC0 1.0 Universal](design/LICENSE) |
| Engineering | [476f649](https://github.com/kochrisdev/TUN-Systemic-Engineering/tree/476f649d41c4a0f659c15276384866908d9b9c01) | Pilot host/provider, contracts, presentation mapping, three schemas | [MIT](engineering/LICENSE) |
| Management | [6959643](https://github.com/kochrisdev/TUN-Systemic-Management/tree/6959643f4ab0134e20d39ae3112a38d501853d05) | Pilot runtime, contracts, schema | [MIT](management/LICENSE) |

The [manifest](manifest.json) lists all 20 selected files with their upstream Git blob identities and commit pins. Paths beneath each component correspond to the same paths in its source repository. Files retain their original licenses; the root Evolution license does not replace them.

Verify the selected text source offline:

```powershell
python scripts/check_vendor.py
```

The checker normalizes CRLF to LF and compares Git blob identities. This establishes correspondence to the recorded blobs, not independent upstream authenticity, security, or general interoperability. The manifest identities were resolved from local clones at the named commits.

Evolution-owned adaptation lives in [the bridge](../reference/tsev_family/bridge.py) and [the renderer](../review/src/Review.tsx). The renderer combines the selected styles and removes their relative token import in the generated HTML; the vendored CSS files themselves remain unchanged. Components are imported directly, without introducing hypothetical companion exports.

For an update, inspect the new upstream source and license, select a deliberate subset, update the manifest and bridge pins together, and rerun the family, renderer, source, and documentation checks. Do not silently follow a moving branch.
