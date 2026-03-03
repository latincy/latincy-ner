"""Convert JSON NER singles to spaCy DocBin files for training."""

from __future__ import annotations

import argparse
import json
import subprocess
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import spacy
from spacy.tokens import DocBin

_MACRON_MAP = str.maketrans("āēīōūȳĀĒĪŌŪȲ", "aeiouyAEIOUY")


def classify_file(path: Path, unsplit_to: str) -> str:
    """Determine whether a file belongs to train, dev, or test split."""
    stem = path.stem
    if stem.endswith("-test"):
        return "test"
    if stem.endswith("-train"):
        return "train"
    if stem.endswith("-dev"):
        return "dev"
    return unsplit_to


def _preprocess(text: str) -> str:
    """Apply the same text normalization as latin_core_tokenizer.preprocess().

    Must stay in sync with LatinTokenizer in latincy-pipelines/scripts/functions.py.
    Steps: ligatures, macrons, accents/diacritics, V→U and J→I.
    """
    text = text.replace("Æ", "Ae").replace("Œ", "Oe").replace("æ", "ae").replace("œ", "oe")
    text = text.translate(_MACRON_MAP)
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("v", "u").replace("V", "U").replace("j", "i").replace("J", "I")
    return text


def load_single(path: Path) -> list[dict]:
    """Load a JSON single and return its data array."""
    with open(path) as f:
        return json.load(f)["data"]


def make_doc(nlp: spacy.Language, item: dict) -> spacy.tokens.Doc:
    """Create a spaCy Doc with entity spans from a data item."""
    doc = nlp.make_doc(_preprocess(item["text"]))
    ents = []
    for span in item["spans"]:
        char_span = doc.char_span(span["start"], span["end"], label=span["label"])
        if char_span is not None:
            ents.append(char_span)
    doc.ents = ents
    return doc


def build(
    collections_dir: Path,
    output_dir: Path,
    unsplit_to: str,
    dedup: bool = True,
) -> None:
    """Scan collections, build DocBins, write to output."""
    nlp = spacy.blank("la")
    files = sorted(collections_dir.rglob("*.json"))

    if not files:
        print(f"No JSON files found in {collections_dir}")
        return

    # Phase 1: Load all items into split buckets with per-file dedup
    raw_splits: dict[str, list[dict]] = {"train": [], "dev": [], "test": []}
    file_counts: dict[str, int] = {"train": 0, "dev": 0, "test": 0}
    file_stats: list[dict] = []  # per-file stats for manifest
    within_dedup_count = 0

    for path in files:
        split = classify_file(path, unsplit_to)
        data = load_single(path)
        file_counts[split] += 1

        n_before = len(data)
        n_ents = sum(len(item.get("spans", [])) for item in data)

        if dedup:
            seen_in_file: set[str] = set()
            deduped = []
            for item in data:
                text = item["text"]
                if text in seen_in_file:
                    within_dedup_count += 1
                    continue
                seen_in_file.add(text)
                deduped.append(item)
            raw_splits[split].extend(deduped)
            n_after = len(deduped)
        else:
            raw_splits[split].extend(data)
            n_after = n_before

        file_stats.append({
            "file": str(path.relative_to(collections_dir)),
            "split": split,
            "sentences": n_after,
            "entities": n_ents,
            "deduped": n_before - n_after,
        })

    # Phase 2: Cross-split dedup (test > dev > train priority)
    cross_dedup_count = 0
    if dedup:
        test_texts = {item["text"] for item in raw_splits["test"]}
        dev_texts = {item["text"] for item in raw_splits["dev"]}
        held_out = test_texts | dev_texts

        filtered_train = []
        for item in raw_splits["train"]:
            if item["text"] in held_out:
                cross_dedup_count += 1
            else:
                filtered_train.append(item)
        raw_splits["train"] = filtered_train

        # Also remove from dev anything that appears in test
        filtered_dev = []
        for item in raw_splits["dev"]:
            if item["text"] in test_texts:
                cross_dedup_count += 1
            else:
                filtered_dev.append(item)
        raw_splits["dev"] = filtered_dev

    # Phase 3: Build DocBins
    splits: dict[str, DocBin] = {"train": DocBin(), "dev": DocBin(), "test": DocBin()}
    counts: dict[str, dict] = {
        "train": {"files": 0, "sents": 0, "ents": 0},
        "dev": {"files": 0, "sents": 0, "ents": 0},
        "test": {"files": 0, "sents": 0, "ents": 0},
    }

    for split_name in ("train", "dev", "test"):
        counts[split_name]["files"] = file_counts[split_name]
        for item in raw_splits[split_name]:
            doc = make_doc(nlp, item)
            splits[split_name].add(doc)
            counts[split_name]["sents"] += 1
            counts[split_name]["ents"] += len(doc.ents)

    output_dir.mkdir(parents=True, exist_ok=True)

    for split_name, docbin in splits.items():
        out_path = output_dir / f"{split_name}.spacy"
        docbin.to_disk(out_path)

    # Phase 4: Write manifest
    git_hash = ""
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=collections_dir,
            text=True,
        ).strip()
    except Exception:
        pass

    version_file = collections_dir.parent.parent / "VERSION"
    corpus_version = ""
    if version_file.exists():
        corpus_version = version_file.read_text().strip()

    manifest = {
        "corpus_version": corpus_version,
        "git_commit": git_hash,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "collections_dir": str(collections_dir),
        "dedup": dedup,
        "totals": {
            "train": counts["train"],
            "dev": counts["dev"],
            "test": counts["test"],
            "within_file_dedup": within_dedup_count,
            "cross_split_dedup": cross_dedup_count,
        },
        "files": file_stats,
    }

    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("Build complete.\n")
    for split_name in ("train", "dev", "test"):
        c = counts[split_name]
        print(
            f"  {split_name}: {c['files']} files, "
            f"{c['sents']} sentences, {c['ents']} entities"
        )

    if dedup:
        print(f"\n  Dedup: {within_dedup_count} within-file duplicates removed")
        print(f"  Dedup: {cross_dedup_count} cross-split overlaps removed")

    out_files = ", ".join(f"{output_dir}/{s}.spacy" for s in ("train", "dev", "test"))
    print(f"\nOutput: {out_files}")
    print(f"Manifest: {manifest_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert JSON NER singles to spaCy DocBin files."
    )
    parser.add_argument(
        "--unsplit-to",
        choices=["train", "dev"],
        default="train",
        help="Where to send files without -train/-dev suffix (default: train)",
    )
    parser.add_argument(
        "--collections-dir",
        type=Path,
        default=Path("assets/collections"),
        help="Source directory (default: assets/collections)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("assets/processed"),
        help="Output directory (default: assets/processed)",
    )
    parser.add_argument(
        "--no-dedup",
        action="store_true",
        help="Disable deduplication (within-file and cross-split)",
    )
    args = parser.parse_args()
    build(args.collections_dir, args.output_dir, args.unsplit_to, dedup=not args.no_dedup)


if __name__ == "__main__":
    main()
