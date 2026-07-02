"""Convert a LatinCy NER/NEL JSON single to spaCy DocBin (.spacy).

Each JSON single (assets/collections/<album>/<work>.json) is a self-contained
annotated dataset. This script converts one file directly — no merging, dedup,
or augmentation. Use scripts/build_training_data.py for the full training
corpus pipeline.

Usage:
    uv run python scripts/ner2spacy.py assets/collections/primer/primer-ritchies-nel.json
    uv run python scripts/ner2spacy.py assets/collections/primer/primer-ritchies-nel.json -o out.spacy
"""

from __future__ import annotations

import argparse
import json
import unicodedata
from pathlib import Path

import spacy
from spacy.tokens import DocBin

_MACRON_MAP = str.maketrans("āēīōūȳĀĒĪŌŪȲ", "aeiouyAEIOUY")


def preprocess(text: str) -> str:
    """Normalize text to match the LatinCy tokenizer pipeline.

    Must stay in sync with LatinTokenizer in latincy-pipelines.
    Steps: ligatures → macrons → diacritics → v/j orthography.
    """
    text = text.replace("Æ", "Ae").replace("Œ", "Oe").replace("æ", "ae").replace("œ", "oe")
    text = text.translate(_MACRON_MAP)
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("v", "u").replace("V", "U").replace("j", "i").replace("J", "I")
    return text


def make_doc(nlp: spacy.Language, item: dict) -> spacy.tokens.Doc:
    """Create a spaCy Doc with entity spans from a single data item."""
    doc = nlp.make_doc(preprocess(item["text"]))
    ents = []
    for span in item.get("spans", []):
        char_span = doc.char_span(span["start"], span["end"], label=span["label"])
        if char_span is not None:
            ents.append(char_span)
    doc.ents = ents
    return doc


def make_bio_lines(doc: spacy.tokens.Doc) -> list[tuple[str, str]]:
    """Return (token_text, BIO_tag) pairs for each token in a Doc."""
    lines = []
    for token in doc:
        if token.ent_iob_ == "B":
            tag = f"B-{token.ent_type_}"
        elif token.ent_iob_ == "I":
            tag = f"I-{token.ent_type_}"
        else:
            tag = "O"
        lines.append((token.text, tag))
    return lines


def convert(items: list[dict], nlp: spacy.Language | None = None) -> DocBin:
    """Convert a list of data items to a spaCy DocBin."""
    if nlp is None:
        nlp = spacy.blank("la")
    db = DocBin()
    for item in items:
        db.add(make_doc(nlp, item))
    return db


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a LatinCy NER/NEL JSON single to a spaCy DocBin."
    )
    parser.add_argument("input", type=Path, help="Path to the JSON single")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output .spacy path (default: <input stem>.spacy alongside input)",
    )
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)["data"]

    out = args.output or args.input.with_suffix(".spacy")
    convert(data).to_disk(out)
    print(f"Wrote {len(data)} docs → {out}")


if __name__ == "__main__":
    main()
