# LatinCy NER

Curated NER training data for [LatinCy](https://huggingface.co/latincy) Latin language models. This repo receives finalized annotation singles from `latincy-ner-annotate` and converts them to spaCy `DocBin` files for model training.

## Collections

| Collection | File | Sentences | Entities |
|---|---|---|---|
| bootstrap | bootstrap-herodotos-train.json | 3,341 | 5,519 |
| bootstrap | bootstrap-herodotos-dev.json | 836 | 1,444 |
| bootstrap | bootstrap-neral-train.json | 444 | 980 |
| bootstrap | bootstrap-neral-dev.json | 111 | 247 |
| nt | nt-matthew.json | 1,069 | 619 |
| ot | ot-genesis.json | 1,522 | 1,962 |
| primer | primer-ritchies.json | 889 | 732 |
| primer | primer-sonnenschein_1902.json | 503 | 385 |
| primer | primer-sonnenschein_1903.json | 332 | 361 |
| ud | ud-train.json | 8,992 | 17,530 |
| ud | ud-dev.json | 2,069 | 4,304 |
| **Total** | **11 files** | **20,108** | **34,083** |

### Corpus Summary

| | Count |
|---|---|
| Sentences | 20,108 |
| Tokens | ~380,000 |
| Entities | 34,083 |

| Label | Count | % |
|---|---|---|
| PERSON | 26,507 | 77.8% |
| LOC | 5,016 | 14.7% |
| NORP | 2,560 | 7.5% |

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Building Training Data

Convert JSON singles to spaCy DocBin files:

```bash
uv run python scripts/build_training_data.py
```

Options:

```
--unsplit-to train|dev    Where unsplit files go (default: train)
--collections-dir PATH    Source directory (default: assets/collections)
--output-dir PATH         Output directory (default: assets/processed)
```

Output: `assets/processed/train.spacy` and `assets/processed/dev.spacy`

## Data Format

Each JSON single has this structure:

```json
{
  "metadata": { "title": "...", "source": "..." },
  "annotation": { "tagset": ["PERSON", "LOC", "NORP"] },
  "data": [
    { "text": "Cato in Sicilia...", "spans": [{"start": 0, "end": 4, "label": "PERSON"}] }
  ]
}
```

Files with `-train` or `-dev` suffix are split accordingly. Unsplit files default to train.
