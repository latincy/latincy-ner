# LatinCy NER

Curated NER training data for [LatinCy](https://huggingface.co/latincy) Latin language models. This repo receives finalized annotation singles from `latincy-ner-annotate` and converts them to spaCy `DocBin` files for model training.

## Entity Types

| Label | Description |
|---|---|
| PERSON | Named individuals (e.g. *Caesar*, *Priamus*) |
| LOC | Geographic locations (e.g. *Roma*, *Sicilia*) |
| NORP | Nationalities, religious, or political groups (e.g. *Romani*, *Christiani*) |

## Collections

Sources are split into train, dev, and test sets. Test files are held-out complete documents for evaluation; train/dev files use 80/20 splits within each source.

| Collection | Source | Split | Sentences | Entities |
|---|---|---|---|---|
| bootstrap | bootstrap-herodotos | train | 2,649 | 5,519 |
| bootstrap | bootstrap-herodotos | dev | 758 | 1,444 |
| bootstrap | bootstrap-neral | test | 555 | 1,227 |
| catena | catena-dcd.1 | train | 459 | 176 |
| catena | catena-dcd.1 | dev | 89 | 23 |
| catena | catena-dcd.2 | test | 334 | 225 |
| nt | nt-matthew | test | 1,069 | 619 |
| ot | ot-genesis | train | 1,203 | 1,575 |
| ot | ot-genesis | dev | 319 | 387 |
| primer | primer-ritchies | train | 699 | 566 |
| primer | primer-ritchies | dev | 190 | 166 |
| primer | primer-sonnenschein_1902 | train | 399 | 288 |
| primer | primer-sonnenschein_1902 | dev | 104 | 97 |
| primer | primer-sonnenschein_1903 | train | 267 | 284 |
| primer | primer-sonnenschein_1903 | dev | 65 | 77 |
| tesserae | tesserae-ovid.metamorphoses.1 | train | 324 | 131 |
| tesserae | tesserae-ovid.metamorphoses.1 | dev | 74 | 28 |
| ud | ud | train | 8,992 | 17,530 |
| ud | ud | dev | 2,069 | 4,304 |

### Totals

| Split | Files | Sentences | Entities |
|---|---|---|---|
| train | 8 | 14,778 | 25,033 |
| dev | 8 | 3,668 | 6,435 |
| test | 3 | 1,958 | 2,071 |
| **Total** | **19** | **20,404** | **33,539** |

Counts are after deduplication (770 within-file, 214 cross-split).

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
--no-dedup                Disable deduplication
```

Output: `assets/processed/{train,dev,test}.spacy` plus `manifest.json` with per-file statistics.

## Data Format

Each JSON single follows this schema:

```json
{
  "metadata": { "title": "...", "source": "..." },
  "annotation": { "tagset": ["PERSON", "LOC", "NORP"] },
  "data": [
    { "text": "Cato in Sicilia...", "spans": [{"start": 0, "end": 4, "label": "PERSON"}] }
  ]
}
```

Files with `-train`, `-dev`, or `-test` suffix are routed to the corresponding split. Unsplit files default to train.

## Preprocessing

Text is normalized before tokenization to match the LatinCy tokenizer pipeline:

1. Ligatures: `æ`→`ae`, `œ`→`oe`
2. Macrons: `ā`→`a`, etc.
3. Diacritics: NFD decompose + strip combining marks
4. Orthography: `v`→`u`, `j`→`i`

## License

The dataset is released under **[CC BY-NC-SA 4.0](LICENSE)** (Attribution–
NonCommercial–ShareAlike). The NER **annotations** are first-party LatinCy work
that would otherwise be CC BY 4.0; the more restrictive umbrella is applied
because several underlying source texts carry NonCommercial / ShareAlike terms,
and licensing the combined collection uniformly honors every source. LatinCy is
a non-commercial academic project, so the NonCommercial clause matches intended
use. This applies equally to the merged exports in `assets/processed/`.

### Source provenance

Each collection embeds source text, so the source license governs
redistribution:

| Collection | Underlying text | Source license |
|---|---|---|
| catena | Augustine, *De Civitate Dei* (The Latin Library) | CC0 (public-domain text) |
| nt / ot | Vulgate (CLTK Tesserae) | CC0 (public-domain text) |
| primer | Ritchie; Sonnenschein 1902/1903 | CC0 (public-domain text) |
| tesserae | Ovid, *Metamorphoses* 1 (CLTK Tesserae) | CC0 (public-domain text) |
| ud | Universal Dependencies Latin treebanks | Mixed: CC BY-NC-SA 2.5/3.0 (Perseus, PROIEL, ITTB, UDante), CC BY-SA 4.0 (LLCT) |
| bootstrap | Herodotos Project / NERAL (silver) | Being reannotated against CC0 Tesserae equivalents; **not for redistribution until that lands** |

The CC0-text collections could individually be released as CC BY 4.0; the
`ud` collection's BY-NC-SA terms are what set the umbrella for the whole dataset.
