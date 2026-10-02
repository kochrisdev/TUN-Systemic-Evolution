"""Verify selected companion source against pinned Git blob identities, offline."""

from hashlib import sha1
import json
from pathlib import Path
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "vendor/manifest.json").read_text(encoding="utf-8"))
    expected = set()
    errors = []
    for entry in manifest["files"]:
        path = root / "vendor" / entry["component"] / entry["path"]
        expected.add(path)
        if not path.is_file():
            errors.append(f"Missing: {path.relative_to(root)}")
            continue
        content = path.read_bytes().replace(b"\r\n", b"\n")
        blob = sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()
        if blob != entry["blob"]:
            errors.append(f"Changed upstream content: {path.relative_to(root)}")
    actual = {p for name in manifest["revisions"] for p in (root / "vendor" / name).rglob("*")
              if p.is_file() and "__pycache__" not in p.parts}
    for path in sorted(actual - expected):
        errors.append(f"Unlisted vendor file: {path.relative_to(root)}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(expected)} selected companion files match pinned Git blobs after CRLF normalization.")
    print("Scope: source identity only; not upstream authenticity, security, or full compatibility.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
