<img src="https://raw.githubusercontent.com/latincy/latincy-ner/main/assets/latincy-ner-logo.jpg" alt="LatinCy NER" width="400">

Curated NER training data for [LatinCy](https://huggingface.co/latincy) Latin language models.

## Named Entity Linking (NEL)

v3.9 adds named entity linking on top of NER: entities in supported singles are linked to external knowledge bases (primarily Wikidata) via a `kb_id` field on each annotated span.

### Album/single model

The corpus is organized as *albums* and *singles*:

- A **single** is one work's complete annotation in a self-contained JSON file — bibliographic metadata, annotation provenance, and annotated sentences.
- An **album** is a thematic collection of related singles (e.g. the `primer` album groups `ritchies`, `sonnenschein_1902`, and `sonnenschein_1903`).

The reference single — `primer/primer-ritchies-nel.json` — is the first complete NER+NEL gold single in the corpus: Ritchie's *Fabulae Faciles* (1904), 909 sentences, 735 spans, 100% linked to Wikidata. Its data card is at `assets/collections/primer/primer-ritchies-datacard.md`.

### Review levels

Each annotation layer carries an independent review level:

| Level | Meaning |
|-------|---------|
| `silver` | Model output, uncorrected |
| `reviewed` | One expert pass; all entities verified |
| `gold` | Two independent passes with adjudication |

The ritchies single has NER at `reviewed` and NEL at `silver`.

### Entity ids and authorities

`kb_id` values are namespaced by authority. Every namespace used must be declared in `annotation.nel.authorities`; `scripts/validate_single.py` enforces this contract (and offset / surface / label integrity) across all singles, with a CI-usable exit code.

| Form | Authority |
|------|-----------|
| `Q130832` | Wikidata (globally dereferenceable) |
| `NIL` / `NIL0042` | dataset-internal; entity has no KB referent |

## Entity Types

| Label | Description |
|---|---|
| PERSON | Named individuals and named collective groups of beings (e.g. *Caesar*, *Argonautae*, *Gorgones*) |
| LOC | Geographic locations (e.g. *Roma*, *Sicilia*) |
| NORP | Nationalities, religious, or political groups (e.g. *Romani*, *Christiani*) |
| MISC | Named individual non-human creatures (e.g. *Cerberus*, *Hydra*) |

`MISC` is **not officially supported in the LatinCy NER tagger**; it is included
here so that an NEL id can be attached to a named token even when it does not
refer to a PERSON, LOC, or NORP.

## Directory layout

```
assets/
  collections/<album>/<work>.json         canonical singles (hand-owned)
  splits/<album>/<work>-{train,dev}.json   deterministic 80/20 train/dev split
  processed/{json,bio}/{train,dev}.*        merged, model-ready training data
```

**`collections/`** is the primary published dataset — the citable, hand-owned singles. This is what you read, study, extend, and cite.

**`splits/`** records the exact train/dev partition used for training, derived deterministically from `collections/` via `scripts/split_unsplit_singles.py` (80/20 hash split) and committed so consumers can reproduce training without any ambiguity about which sentences land where. Test sets are held-out complete documents — a single whose metadata declares `"split": "test"` is written unsplit as a `-test` file and never hash-split; **this release ships no test set.**

**`processed/`** is the merged, deduplicated, model-ready corpus built from `splits/` by `python main.py`. It adds cross-source deduplication and casing augmentation on top of the raw splits. Committed for convenience — anyone training a LatinCy model can use it directly without running the build pipeline.

## Collections

| Collection | Source | Split | Sentences | Entities |
|---|---|---|---|---|
| primer | primer-ritchies-nel | train | 730 | 587 |
| primer | primer-ritchies-nel | dev | 179 | 148 |
| primer | primer-sonnenschein_1902 | train | 399 | 288 |
| primer | primer-sonnenschein_1902 | dev | 104 | 97 |
| primer | primer-sonnenschein_1903 | train | 267 | 284 |
| primer | primer-sonnenschein_1903 | dev | 65 | 77 |

### Totals

| Split | Files | Sentences | Entities |
|---|---|---|---|
| train | 3 | 1,396 | 1,159 |
| dev | 3 | 348 | 322 |
| **Total** | **6** | **1,744** | **1,481** |

Counts exclude casing augmentation (train only; +1,183 variants at build time).

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Building Training Data

Convert JSON singles to model-ready training files:

```bash
uv run python main.py
```

Options:

```
--unsplit-to train|dev    Where unsplit files go (default: train)
--collections-dir PATH    Source directory (default: assets/collections)
--output-dir PATH         Output directory (default: assets/processed)
--no-dedup                Disable deduplication
```

Output: `assets/processed/json/{train,dev,test}.json` and `assets/processed/bio/{train,dev,test}.tsv` plus `assets/processed/manifest.json` with per-file statistics.

## Data Format

Each JSON single has three top-level keys:

```json
{
  "metadata": { "title": "...", "source": "...", "version": "0.2.0", ... },
  "annotation": { "tagset": ["PERSON", "LOC", "NORP", "MISC"], ... },
  "data": [
    {
      "text": "Perseus autem in insulam Seriphum pervenit.",
      "spans": [
        {"start": 0, "end": 7, "label": "PERSON", "surface": "Perseus", "kb_id": "Q130832"},
        {"start": 25, "end": 33, "label": "LOC", "surface": "Seriphum", "kb_id": "Q217214"}
      ]
    }
  ]
}
```

NEL singles add `surface` (the inflected form, `text[start:end]`) and `kb_id`
(a Wikidata `Q…` or `NIL`) to each span; NER-only
singles carry just `start`, `end`, `label`.

### `metadata` fields

| Field | Description |
|-------|-------------|
| `title`, `author`, `date` | Bibliographic identity of the source work |
| `version` | Semantic version of this single |
| `source` | URL of the source text |
| `latincy-ner-project` | Album the single belongs to |
| `latincy-ner-project-subset` | Work identifier within the album |
| `language` | ISO code (`la`) |
| `genre` | e.g. `prose`, `verse` |
| `source_license` | License of the underlying text |
| `annotation_license` | License of the annotation layer |

### `annotation` fields

Provenance for each processing layer. NER-only singles omit the `nel` block.

```json
"annotation": {
  "segmentation": {"senter_model": "la_core_web_lg", "senter_version": "3.9.4"},
  "ner": {"spacy_model": "la_core_web_lg", "spacy_model_version": "3.9.4",
          "review_level": "reviewed"},
  "nel": {
    "authorities": [{"prefix": "wd", "name": "Wikidata", "snapshot": "2026-06-15"}],
    "method": "wikidata_kb candidates + claude-opus-4-8 bootstrapping",
    "review_level": "silver"
  },
  "tagset": ["PERSON", "LOC", "NORP", "MISC"],
  "annotators": ["Patrick J. Burns"]
}
```

Files with `-train`, `-dev`, or `-test` suffix are routed to the corresponding split. Unsplit files default to train.

## Provenance

The models used for sentence segmentation, tokenization, and annotation are
recorded per single in each file's `annotation` block (see [Data Format](#data-format)).

## License

`latincy-ner` is a **collection of independently-licensed datasets**. Each single
carries its own rights statement in its `metadata` block, and those fields are
authoritative:

- `source_license` — license of the underlying source text
- `annotation_license` — license of the LatinCy annotation layer

**Unless a single states otherwise, its contents are released under
[CC BY-NC-SA 4.0](LICENSE)** (Attribution–NonCommercial–ShareAlike), the
repository default recorded in `LICENSE`.

### This release

| Single | Source text | `source_license` | `annotation_license` |
|---|---|---|---|
| `primer/ritchies` | Ritchie, *Fabulae Faciles* (1904), via The Latin Library | CC0 | CC BY 4.0 |
| `primer/sonnenschein_1902` | Sonnenschein, *Ora Maritima* (1902) | CC0 | CC BY 4.0 |
| `primer/sonnenschein_1903` | Sonnenschein, *Pro Patria* (1903) | CC0 | CC BY 4.0 |

Only `primer/ritchies` carries NEL links and a reviewed NER pass; the other
singles are NER-only at `review_level: silver` (each single's `annotation` block
states its own level).
