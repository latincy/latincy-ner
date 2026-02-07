"""Convert JSON NER singles to spaCy DocBin files for training."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import spacy
from spacy.tokens import DocBin


def classify_file(path: Path, unsplit_to: str) -> str:
    """Determine whether a file belongs to train or dev split."""
    stem = path.stem
    if stem.endswith("-train"):
        return "train"
    if stem.endswith("-dev"):
        return "dev"
    return unsplit_to


def load_single(path: Path) -> list[dict]:
    """Load a JSON single and return its data array."""
    with open(path) as f:
        return json.load(f)["data"]


def make_doc(nlp: spacy.Language, item: dict) -> spacy.tokens.Doc:
    """Create a spaCy Doc with entity spans from a data item."""
    doc = nlp.make_doc(item["text"])
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
) -> None:
    """Scan collections, build DocBins, write to output."""
    nlp = spacy.blank("la")
    files = sorted(collections_dir.rglob("*.json"))

    if not files:
        print(f"No JSON files found in {collections_dir}")
        return

    splits: dict[str, DocBin] = {"train": DocBin(), "dev": DocBin()}
    counts: dict[str, dict] = {
        "train": {"files": 0, "sents": 0, "ents": 0},
        "dev": {"files": 0, "sents": 0, "ents": 0},
    }

    for path in files:
        split = classify_file(path, unsplit_to)
        data = load_single(path)
        counts[split]["files"] += 1

        for item in data:
            doc = make_doc(nlp, item)
            splits[split].add(doc)
            counts[split]["sents"] += 1
            counts[split]["ents"] += len(doc.ents)

    output_dir.mkdir(parents=True, exist_ok=True)

    for split_name, docbin in splits.items():
        out_path = output_dir / f"{split_name}.spacy"
        docbin.to_disk(out_path)

    print("Build complete.\n")
    for split_name in ("train", "dev"):
        c = counts[split_name]
        print(
            f"  {split_name}: {c['files']} files, "
            f"{c['sents']} sentences, {c['ents']} entities"
        )
    print(f"\nOutput: {output_dir}/train.spacy, {output_dir}/dev.spacy")


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
    args = parser.parse_args()
    build(args.collections_dir, args.output_dir, args.unsplit_to)


if __name__ == "__main__":
    main()
