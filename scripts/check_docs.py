"""Check relative Markdown file links, fenced blocks, and requirement inventory.

No external URLs or anchors are checked. Passing does not validate product claims.
"""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    files = sorted(root.rglob("*.md"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"^```", text, re.MULTILINE)) % 2:
            errors.append(f"{path.relative_to(root)}: unmatched code fence")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            parts = urlsplit(target)
            if parts.scheme or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f"{path.relative_to(root)}: missing or out-of-bundle link: {target}")
    specification = (root / "docs/SPECIFICATION-v0.1.md").read_text(encoding="utf-8")
    ids = re.findall(r"^## (TSEV-\d{3})", specification, re.MULTILINE)
    if ids != [f"TSEV-{n:03}" for n in range(1, 13)]:
        errors.append("specification: expected exactly TSEV-001 through TSEV-012 in order")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(files)} Markdown files; local file links, code fences, and 12 requirement headings.")
    print("Scope: external URLs, anchors, normative completeness, and product claims are not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
