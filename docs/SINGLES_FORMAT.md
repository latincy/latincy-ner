# LatinCy NER + NEL Singles — Dataset Format

This document specifies the format and conventions of the LatinCy gold-standard
Named Entity Recognition (NER) and Named Entity Linking (NEL) datasets.

## The album / single model

A **single** is one work's complete annotation in a self-describing JSON file:
a bibliographic `metadata` header, an `annotation` provenance header, and a
`data` array of annotated sentences. Singles are the unit of development and
publication — you annotate one work, version it, and publish it independently,
the way a recording artist releases a single.

An **album** is a `latincy-ner-project` — a collection of related singles
(e.g. `primer` groups `ritchies`, `sonnenschein_1902`, `sonnenschein_1903`).

## Directory layout

```
assets/
  collections/<album>/<work>.json   ← canonical singles (hand-owned)
  splits/<album>/<work>-{train,dev}.json   ← derived 80/20 splits
  processed/{json,bio}/{train,dev,test}.*  ← merged, model-ready training data
```

- **`collections/`** holds the canonical singles. This is the published dataset.
- **`splits/`** is derived from `collections/` by a deterministic hash split
  (`scripts/split_unsplit_singles.py`). Never hand-edit.
- **`processed/`** is the merged, deduplicated, model-ready corpus built from
  `splits/` (`scripts/build_training_data.py`). Never hand-edit.

Only `collections/` is hand-owned; everything else regenerates.

## Single schema

```json
{
  "metadata": { ... },
  "annotation": { ... },
  "data": [ { "text": "...", "spans": [ ... ] } ]
}
```

### `metadata`

| Field | Description |
|-------|-------------|
| `title`, `author`, `date` | Bibliographic identity of the source work |
| `version` | Semantic version of *this single* (see Versioning) |
| `source` | URL of the source text |
| `latincy-ner-project` | Album the single belongs to |
| `latincy-ner-project-subset` | The work's identifier within the album |
| `language` | ISO code (`la`) |
| `genre` | e.g. `prose`, `verse` |
| `source_license` | License of the underlying text (often public domain / CC0) |
| `annotation_license` | License of the annotation labor (e.g. CC BY 4.0) |

### `annotation`

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

- **`segmentation`** records the senter model + version. Source sentences are a
  *derived, versioned* artifact: re-segmentation changes offsets and is a
  deliberate operation, not a silent rerun.
- **`ner`** / **`nel`** each carry their own `review_level` — these layers can
  differ in maturity within one single.
- **`authorities`** declares the namespaces that `kb_id`s resolve against (see
  below). Only the entity catalog travels with the dataset; candidate lookup
  tables do not.

#### Review-level vocabulary

| Level | Meaning |
|-------|---------|
| `silver` | Model output, uncorrected |
| `reviewed` | One expert pass; all entities verified |
| `gold` | Two independent passes with adjudication |

### `data` and `spans`

Each `data` item is one sentence in source running order. Sentences with no
entities are included with an empty `spans` array (they are NER negatives).

```json
{
  "text": "Perseus autem in insulam Seriphum pervenit.",
  "spans": [
    {"start": 0, "end": 7, "label": "PERSON", "surface": "Perseus", "kb_id": "Q127367"},
    {"start": 23, "end": 30, "label": "LOC", "surface": "Seriphum", "kb_id": "Q216736"}
  ]
}
```

| Span field | Description |
|------------|-------------|
| `start`, `end` | Character offsets into `text` (`text[start:end]`) |
| `label` | One of the tagset labels |
| `surface` | The inflected form as it appears: `text[start:end]` (NEL singles) |
| `kb_id` | Entity id, or `null` for NIL (NEL singles only) |

NER-only singles carry only `start`, `end`, `label`.

## Entity ids and authorities

`kb_id` values are namespaced by authority:

| Form | Authority | Resolution |
|------|-----------|------------|
| `Q130832` | Wikidata | globally dereferenceable (wikidata.org) |
| `lkb:<type>:<source>:<id>` | local LatinCy catalog | resolves against the published `latincy-entities` catalog |
| `NIL` / `NIL0042` | dataset-internal | entity not in any KB; NIL clusters share an id across mentions |

`NIL` ("Not In Lexicon") is standard NEL terminology (CoNLL, TAC-KBP, AIDA). A
span is NIL only when the entity genuinely has no KB referent — never merely
because it was hard to identify.

**Invariant — declared authorities cover used ids.** Every `kb_id` namespace a
single actually uses (`wd` for Q-ids, `lkb` for catalog ids) must be declared in
`annotation.nel.authorities`. `NIL` is dataset-internal and needs no
declaration. This is what makes a published id resolvable to an outside
consumer; `scripts/validate_single.py` enforces it (and offset/surface/label
integrity) across all singles, with a CI-usable exit code.

## Entity labels

| Label | Description |
|-------|-------------|
| PERSON | Named individuals and named mythological/ethnic *groups* (e.g. *Argonautae*, *Gorgones*) |
| LOC | Places, rivers, geographic features |
| NORP | Peoples and ethnic/cultural groups (e.g. *Graeci*, *Romani*) |
| MISC | Named individual non-human creatures (e.g. *Cerberus*, *Hydra*) |

Guideline: a named *collective* of beings is PERSON; a named *individual*
creature is MISC. When a NORP group has no Wikidata entry, link to the most
specific associated entity (e.g. *Thebani* → Thebes Q11225429).

## Versioning

Each single is versioned independently with [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking change to consumers (e.g. re-segmentation that changes
  offsets; schema change).
- **MINOR** — additive (e.g. adding NEL links or a new label to existing spans).
- **PATCH** — fixes (e.g. a corrected link, an OCR fix).

A *remaster* is a significant version bump that reissues the same work with
improved production (re-segmentation, added annotation layers). Example:
`ritchies` v0.1 (NER-only) → v0.2.0 (remastered NER+NEL).

## Provenance pipeline

A single is produced bootstrap-data → published-dataset via:
segmentation (senter) → NER (model + Prodigy review) → NEL (KB candidates +
bootstrapping, Prodigy adjudication) → stamp → publish. Derived `splits/` and
`processed/` rebuild downstream. See the architecture plan in the `latincy-nel`
repo for the full runbook.
