"""Validate NER/NEL singles for structural integrity and id resolvability.

Checks every single under assets/collections/ (or a given path) against the
SINGLES_FORMAT contract. The Phase-3 invariant this enforces:

    Every kb_id namespace a single actually uses MUST be declared in
    annotation.nel.authorities.

That is what makes a published single's ids meaningful to anyone who is not us:
a `wd` id resolves at Wikidata; an `lkb:` id resolves against a versioned
latincy-entities catalog; `NIL` is dataset-internal. A single that links spans
to an authority it never declares is shipping unresolvable references.

Also validates (per single):
  - required top-level keys: metadata, annotation, data
  - spans: start/end in range, label in the declared tagset
  - NEL singles: surface == text[start:end] (offsets are exact)

Exit code is non-zero if any single fails, so this is CI-usable.

Usage:
  python scripts/validate_single.py                  # all singles
  python scripts/validate_single.py assets/collections/primer/primer-ritchies-nel.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS = REPO_ROOT / "assets" / "collections"

# kb_id namespaces that are dataset-internal and need no external authority.
# NIL ("Not In Lexicon") clusters are intrinsic to NEL annotation.
INTERNAL_PREFIXES = {"NIL"}


def kb_id_prefix(kb_id: str) -> str:
    """Authority prefix for a kb_id. Q-ids → 'wd'; lkb:… → 'lkb'; NIL… → 'NIL'."""
    if kb_id.startswith("lkb:"):
        return "lkb"
    if kb_id.startswith("NIL"):
        return "NIL"
    if kb_id.startswith("Q") and kb_id[1:].isdigit():
        return "wd"
    return kb_id.split(":", 1)[0]  # unknown — return as-is for reporting


def validate_single(path: Path) -> list[str]:
    """Return a list of error strings for one single (empty == valid)."""
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return [f"unreadable: {e}"]

    for key in ("metadata", "annotation", "data"):
        if key not in data:
            errors.append(f"missing top-level key: {key!r}")
    if errors:
        return errors

    annotation = data["annotation"]
    tagset = set(annotation.get("tagset", []))
    if not tagset:
        errors.append("annotation.tagset is empty or missing")

    nel = annotation.get("nel")
    declared = {a["prefix"] for a in nel.get("authorities", [])} if nel else set()

    used_prefixes: set[str] = set()
    for i, item in enumerate(data["data"]):
        text = item.get("text", "")
        for s in item.get("spans", []):
            start, end, label = s.get("start"), s.get("end"), s.get("label")
            loc = f"sent {i} [{start}:{end}]"
            if not isinstance(start, int) or not isinstance(end, int):
                errors.append(f"{loc}: non-integer offsets")
                continue
            if not (0 <= start < end <= len(text)):
                errors.append(f"{loc}: offsets out of range (len={len(text)})")
            if label not in tagset:
                errors.append(f"{loc}: label {label!r} not in tagset")
            if "surface" in s and text[start:end] != s["surface"]:
                errors.append(
                    f"{loc}: surface {s['surface']!r} != text slice "
                    f"{text[start:end]!r}"
                )
            kb_id = s.get("kb_id")
            if kb_id is not None:
                used_prefixes.add(kb_id_prefix(kb_id))

    # The Phase-3 invariant: usage ⊆ (declared ∪ internal).
    undeclared = used_prefixes - declared - INTERNAL_PREFIXES
    for p in sorted(undeclared):
        errors.append(
            f"kb_id namespace {p!r} used in spans but not declared in "
            f"annotation.nel.authorities"
        )
    # Soft warning surfaced as info: declared but unused authorities are fine
    # (e.g. a catalog declared defensively), so we do not flag them.

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="single JSON files to validate (default: all under collections/)",
    )
    args = ap.parse_args()

    if args.paths:
        singles = args.paths
    else:
        singles = sorted(
            p
            for p in COLLECTIONS.rglob("*.json")
            if not p.stem.endswith(("-train", "-dev", "-test"))
        )

    failed = 0
    for path in singles:
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        errs = validate_single(path)
        if errs:
            failed += 1
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"        - {e}")
        else:
            print(f"ok    {rel}")

    print(f"\n{len(singles) - failed}/{len(singles)} singles valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
