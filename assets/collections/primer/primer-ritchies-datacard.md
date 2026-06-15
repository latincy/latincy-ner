# Data Card: Fabulae Faciles NER + NEL (`ritchies`)

**Version 0.2.0** — *remastered* edition. v0.1 was NER-only; v0.2.0 adds Named
Entity Linking, the MISC label, a from-scratch re-segmentation
(`la_core_web_lg` 3.9.4), and an OCR correction (*Octam* → *Oetam*).

## Dataset Summary

Gold-standard Named Entity Recognition (NER) and silver Named Entity Linking
(NEL) annotations for Ritchie's *Fabulae Faciles* (1904 ed.), a widely-used
Latin reader covering the myths of Perseus, Hercules, and Jason. Entities are
linked to Wikidata QIDs.

- **Sentences:** 909 (source); 504 carry at least one entity
- **Named entity spans:** 735
- **Linked to Wikidata:** 735 (100%)
- **NIL (intentionally unlinked):** 0
- **Entity labels:** PERSON, LOC, NORP, MISC

## Source Text

Ritchie, F. (1904). *Fabulae Faciles: A First Latin Reader*. Public domain. Text
sourced from [the Latin Library](https://www.thelatinlibrary.com/ritchie.html).

## Annotation

| Layer | Tooling | Review level |
|-------|---------|--------------|
| Segmentation | `la_core_web_lg` 3.9.4 senter | — |
| NER | `la_core_web_lg` 3.9.4, then [Prodigy](https://prodi.gy) | **reviewed** (full expert pass, one annotator) |
| NEL | Wikidata-KB candidates + `claude-opus-4-8` bootstrapping, adjudicated in Prodigy | **silver** (one annotator) |

Annotator: Patrick J. Burns.

**Review-level vocabulary.** `silver` = model output, uncorrected; `reviewed` =
one expert pass with all entities verified; `gold` = two independent passes with
adjudication. NER here is `reviewed`; NEL is `silver`.

## Authorities

Entity ids resolve against:

| Prefix | Authority | Snapshot |
|--------|-----------|----------|
| `wd` | Wikidata | 2026-06-15 |

This single is **100% Wikidata** (zero NIL, zero local ids), so it carries no
dependency on the forthcoming `latincy-entities` catalog.

## Entity Labels

| Label | Count | Description |
|-------|-------|-------------|
| PERSON | 578 | Named individuals and named groups (e.g., *Argonautae*, *Gorgones*) |
| LOC | 103 | Places, rivers, geographic features |
| NORP | 51 | Peoples and ethnic/cultural groups (e.g., *Graeci*, *Romani*) |
| MISC | 3 | Named individual non-human creatures (e.g., *Cerberus*, *Hydra*) |

## NIL Policy

All 735 spans are linked; NIL is defined but unused in this dataset. A span would
be NIL when:

1. **Not a real entity** — the surface form is not a proper name referencing a
   unique individual (e.g., *Neminem*, "Nobody," Odysseus's trick name to the
   Cyclops).
2. **Genuinely unresolvable** — a generic epithet used as a proper name with no
   specific referent in any knowledge base.

NIL is **not** used for entities that were merely hard to identify; those were
resolved by the annotator. Spans that turned out to be descriptive phrases
(*domum Circaeam*, *oraculum Delphicum*) were removed from the annotation
entirely.

**NIL** is standard NEL terminology (CoNLL, TAC-KBP, AIDA shared tasks): "Not In
Lexicon" — the entity cannot be linked to any KB entry.

## Annotation Guidelines

### Mythological collectives vs. individual creatures

- **Named groups of mythological beings** → PERSON: *Gorgones*, *Graiae*,
  *Hesperides*, *Amazones*.
- **Named individual non-human creatures** → MISC: *Cerberus* (Q83496), *Hydra*
  (Q83040).

### NORP entities when the group has no Wikidata entry

When a people/ethnic-group entity (NORP) has no dedicated Wikidata entry, link to
the specific associated entity instead (e.g., *Thebani* → Thebes Q11225429 rather
than leaving as NIL). Prefer the most specific available entry.

## Files

| File | Description |
|------|-------------|
| `primer-ritchies-nel.json` | **Canonical single** — sentences in running order, full `metadata`/`annotation` header, spans with `start, end, label, surface, kb_id` |
| `../../splits/primer/primer-ritchies-nel-{train,dev}.json` | Derived 80/20 training splits (latincy-ner format) |

### Single span format

```json
{
  "text": "Perseus autem in insulam Seriphum pervenit.",
  "spans": [
    {"start": 0, "end": 7, "label": "PERSON", "surface": "Perseus", "kb_id": "Q127367"},
    {"start": 23, "end": 30, "label": "LOC", "surface": "Seriphum", "kb_id": "Q216736"}
  ]
}
```

`surface` is the inflected form as it appears in the text (`text[start:end]`); a
null `kb_id` would mean NIL (none in this dataset).

## License

- **Source text:** public domain (Ritchie 1904).
- **Annotations:** CC BY 4.0.

## Citation

Burns, P.J. (2026). *Fabulae Faciles NER+NEL Gold Dataset* (`ritchies` v0.2.0).
LatinCy project. https://github.com/diyclassics/latincy-ner
