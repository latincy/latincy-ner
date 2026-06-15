#!/usr/bin/env python3
"""Build NER annotations for UDante test sentences 0:122.

Annotations were decided manually per ANNOTATION_RULES.md (PERSON/LOC/NORP).
This script computes char offsets deterministically with str.find (first
occurrence), marks "multi": true when a surface occurs more than once, and
DROPS + logs any surface that is not an exact substring of its sentence text.
"""
import json
import sys
from pathlib import Path

SRC = Path("/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-udante-test.json")
OUT = Path("/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/udante_0_122.json")

# Manual (surface, label) decisions keyed by data index.
# Surfaces copied char-for-char from each sentence text.
ANNOT = {
    3: [("Romani", "NORP")],
    4: [("Greci", "NORP")],
    23: [("Ouidius", "PERSON")],
    40: [("Genesis", "LOC")],  # excluded below (book title) -> handled by note; remove
    43: [("Ade", "PERSON"), ("Eo", "PERSON")],
    62: [("Petramala", "LOC"), ("Adam", "PERSON")],
    63: [("Ade", "PERSON")],
    64: [("Sarnum", "LOC"), ("Florentiam", "LOC")],
    65: [("Florentia", "LOC"), ("Tusciam", "LOC"), ("Florentiam", "LOC"), ("Latinos", "NORP")],
    68: [("Adam", "PERSON")],
    69: [("Babel", "LOC")],
    70: [("Heber", "PERSON"), ("Hebrei", "NORP")],
    72: [("hebraicum", "NORP")],
    82: [("Nembroth", "PERSON"), ("Sennaar", "LOC"), ("Babel", "LOC")],
    94: [("Sem", "PERSON"), ("Noe", "PERSON"), ("Israel", "NORP")],
    96: [("Europe", "LOC")],
    97: [("Europam", "LOC")],
    98: [("Europa", "LOC")],
    99: [("Grecos", "NORP"), ("Europe", "LOC"), ("Asye", "LOC")],
    101: [("Danubii", "LOC"), ("Meotidis", "LOC"), ("Anglie", "LOC"),
          ("Oceano", "LOC"),
          ("Ytalorum", "NORP"), ("Francorum", "NORP"),
          ("Sclauones", "NORP"), ("Ungaros", "NORP"), ("Teutonicos", "NORP"),
          ("Saxones", "NORP"), ("Anglicos", "NORP")],
    102: [("Ungarorum", "NORP"), ("Europa", "LOC")],
    103: [("Europa", "LOC")],
    104: [("Yspani", "NORP"), ("Franci", "NORP"), ("Latini", "NORP")],
    106: [("Europe", "LOC"), ("Ianuensium", "NORP")],
    107: [("Ytalie", "LOC"), ("Adriatici", "LOC"), ("Siciliam", "LOC")],
    109: [("Alamannos", "NORP"), ("Aragonie", "LOC")],
    110: [("Prouincialibus", "NORP"), ("Apenini", "LOC")],
    115: [("Babel", "LOC")],
    117: [("Gerardus de Brunel", "PERSON")],
    118: [("Nauarre", "LOC")],
    119: [("Guido Guinizelli", "PERSON")],
    121: [("Ytalie", "LOC"), ("Paduani", "NORP"), ("Pisani", "NORP")],
}

# Drop the Genesis book-title decision (rules: do NOT tag works/books).
ANNOT[40] = []


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"][0:122]

    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for i, item in enumerate(data):
        text = item["text"]
        sent_id = item["meta"]["sent_id"]
        ents = []
        for surface, label in ANNOT.get(i, []):
            start = text.find(surface)
            if start == -1:
                dropped.append((i, sent_id, surface, label))
                continue
            end = start + len(surface)
            multi = text.count(surface) > 1
            ents.append({
                "text": surface,
                "label": label,
                "start": start,
                "end": end,
                "multi": multi,
            })
            counts[label] += 1
        out.append({"sent_id": sent_id, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    total = sum(counts.values())
    print(f"TOTAL ENTITIES: {total}")
    if dropped:
        print("DROPPED (non-substring surfaces):", file=sys.stderr)
        for i, sid, surf, lab in dropped:
            print(f"  [{i}] {sid}: {surf!r} ({lab})", file=sys.stderr)
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
