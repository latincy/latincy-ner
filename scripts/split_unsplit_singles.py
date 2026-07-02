"""Split unsplit NER singles into deterministic train/dev files.

Reads canonical singles from assets/collections/, writes splits to the
corresponding subfolder under assets/splits/. The source file is not
modified.

Uses hash-based splitting (80/20) to create reproducible train/dev splits.
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


def split_file(path: Path, splits_dir: Path, dry_run: bool = False) -> dict:
    """Split a single into train/dev — or emit a whole-document test set.

    A single whose metadata declares ``"split": "test"`` is a held-out
    evaluation document: it is written unsplit as ``<stem>-test.json`` and is
    NOT hash-split into train/dev. Every other single is hash-split 80/20.
    """
    with open(path) as f:
        data = json.load(f)

    metadata = data["metadata"]
    annotation = data["annotation"]
    items = data["data"]
    stem = path.stem
    subset = metadata.get("latincy-ner-project-subset", stem)

    if metadata.get("split") == "test":
        partitions = [("test", items)]
    else:
        train_items, dev_items = [], []
        for item in items:
            (dev_items if hash_split(item["text"]) == "dev" else train_items).append(item)
        partitions = [("train", train_items), ("dev", dev_items)]

    stats = {"file": path.name, "total": len(items), "train": 0, "dev": 0, "test": 0}
    for name, its in partitions:
        stats[name] = len(its)

    if dry_run:
        return stats

    out_dir = splits_dir / path.parent.name
    out_dir.mkdir(parents=True, exist_ok=True)

    for split_name, split_items in partitions:
        out_path = out_dir / f"{stem}-{split_name}.json"
        out_data = {
            "metadata": {
                **metadata,
                "latincy-ner-project-subset": f"{subset}-{split_name}",
                "split_from": path.name,
            },
            "annotation": annotation,
            "data": split_items,
        }
        with open(out_path, "w") as f:
            json.dump(out_data, f, indent=2, ensure_ascii=False)

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
    parser.add_argument(
        "--splits-dir",
        type=Path,
        default=Path("assets/splits"),
        help="Output directory for splits (default: assets/splits)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show splits without writing")
    args = parser.parse_args()

    files = sorted(args.collections_dir.rglob("*.json"))
    unsplit = [f for f in files if is_unsplit(f)]

    if not unsplit:
        print("No unsplit files found.")
        return

    print(f"Found {len(unsplit)} unsplit files:\n")
    print(f"{'File':<45} {'Total':>6} {'Train':>6} {'Dev':>6} {'Test':>6}")
    print("-" * 78)

    total_train = total_dev = total_test = 0

    for path in unsplit:
        stats = split_file(path, args.splits_dir, dry_run=args.dry_run)
        total_train += stats["train"]
        total_dev += stats["dev"]
        total_test += stats["test"]
        print(f"{stats['file']:<45} {stats['total']:>6} {stats['train']:>6} {stats['dev']:>6} {stats['test']:>6}")

    print("-" * 78)
    print(f"{'TOTAL':<45} {total_train + total_dev + total_test:>6} {total_train:>6} {total_dev:>6} {total_test:>6}")

    if args.dry_run:
        print("\n(Dry run — no files written)")
    else:
        print(f"\nSplit complete. Original files renamed to .json.orig")


if __name__ == "__main__":
    main()
