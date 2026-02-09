"""Split unsplit NER singles into deterministic train/dev files.

Uses hash-based splitting (80/20) to create reproducible train/dev
splits for source files that lack -train/-dev suffixes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


DEV_RATIO = 5  # 1 in 5 → 20% dev


def hash_split(text: str) -> str:
    """Deterministic split based on text hash. Returns 'dev' or 'train'."""
    h = int(hashlib.sha256(text.encode()).hexdigest(), 16)
    return "dev" if h % DEV_RATIO == 0 else "train"


def is_unsplit(path: Path) -> bool:
    """True if the file has no -train or -dev suffix."""
    stem = path.stem
    return not stem.endswith("-train") and not stem.endswith("-dev")


def split_file(path: Path, dry_run: bool = False) -> dict:
    """Split a single JSON file into train and dev versions."""
    with open(path) as f:
        data = json.load(f)

    metadata = data["metadata"]
    annotation = data["annotation"]
    items = data["data"]

    train_items = []
    dev_items = []

    for item in items:
        if hash_split(item["text"]) == "dev":
            dev_items.append(item)
        else:
            train_items.append(item)

    stem = path.stem
    parent = path.parent

    stats = {
        "file": path.name,
        "total": len(items),
        "train": len(train_items),
        "dev": len(dev_items),
    }

    if dry_run:
        return stats

    for split_name, split_items in [("train", train_items), ("dev", dev_items)]:
        out_path = parent / f"{stem}-{split_name}.json"
        out_data = {
            "metadata": {
                **metadata,
                "latincy-ner-project-subset": f"{metadata.get('latincy-ner-project-subset', stem)}-{split_name}",
                "split_from": path.name,
            },
            "annotation": annotation,
            "data": split_items,
        }
        with open(out_path, "w") as f:
            json.dump(out_data, f, indent=2, ensure_ascii=False)

    # Rename original to .orig
    orig_path = path.with_suffix(".json.orig")
    path.rename(orig_path)

    return stats


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Split unsplit NER singles into train/dev.")
    parser.add_argument(
        "--collections-dir",
        type=Path,
        default=Path("assets/collections"),
        help="Source directory (default: assets/collections)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show splits without writing")
    args = parser.parse_args()

    files = sorted(args.collections_dir.rglob("*.json"))
    unsplit = [f for f in files if is_unsplit(f)]

    if not unsplit:
        print("No unsplit files found.")
        return

    print(f"Found {len(unsplit)} unsplit files:\n")
    print(f"{'File':<45} {'Total':>6} {'Train':>6} {'Dev':>6}")
    print("-" * 70)

    total_train = 0
    total_dev = 0

    for path in unsplit:
        stats = split_file(path, dry_run=args.dry_run)
        total_train += stats["train"]
        total_dev += stats["dev"]
        print(f"{stats['file']:<45} {stats['total']:>6} {stats['train']:>6} {stats['dev']:>6}")

    print("-" * 70)
    print(f"{'TOTAL':<45} {total_train + total_dev:>6} {total_train:>6} {total_dev:>6}")

    if args.dry_run:
        print("\n(Dry run — no files written)")
    else:
        print(f"\nSplit complete. Original files renamed to .json.orig")


if __name__ == "__main__":
    main()
