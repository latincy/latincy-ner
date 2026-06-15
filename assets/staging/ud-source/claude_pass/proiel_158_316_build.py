#!/usr/bin/env python3
"""Build NER annotations for PROIEL test data[158:316] (Vulgate, Luke).

Deterministic offsets via str.find (first occurrence default; multi:true if >1;
DROP + log any surface that is not an exact substring of the sentence text).
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/proiel_158_316.json")

# Per-sent_id (surface, label) decisions. Surfaces copied EXACTLY from text.
ANN = {
    "16658": [("Pharisaeorum", "NORP")],
    "16660": [("Iesus", "PERSON")],
    "16661": [("Dauid", "PERSON")],
    "16668": [("Pharisaei", "NORP")],
    "16673": [("Iesus", "PERSON")],
    "16680": [("Iesu", "PERSON")],
    "16683": [
        ("Simonem", "PERSON"),
        ("Petrum", "PERSON"),
        ("Andream", "PERSON"),
        ("Iacobum", "PERSON"),     # multi (Iacobum appears twice)
        ("Iohannem", "PERSON"),
        ("Philippum", "PERSON"),
        ("Bartholomeum", "PERSON"),
        ("Mattheum", "PERSON"),
        ("Thomam", "PERSON"),
        ("Alphei", "PERSON"),
        ("Iudam", "PERSON"),       # multi (Iudam appears twice)
        ("Scarioth", "PERSON"),
    ],
    "48097": [
        ("Iudaea", "LOC"),
        ("Hierusalem", "LOC"),
        ("Tyri", "LOC"),
        ("Sidonis", "LOC"),
    ],
    "17636": [],  # mamonae = personified wealth; not a proper individual -> skip
    "17637": [("Pharisaei", "NORP")],
    "17643": [("Iohannem", "PERSON")],
    "17649": [("Lazarus", "PERSON")],
    "17651": [("Abrahae", "PERSON")],
    "17653": [("Abraham", "PERSON"), ("Lazarum", "PERSON")],
    "17655": [("Abraham", "PERSON"), ("Lazarum", "PERSON")],
    "17656": [("Abraham", "PERSON")],
    "17657": [("Lazarus", "PERSON")],
    "17665": [("Abraham", "PERSON")],
    "17666": [("Mosen", "PERSON")],
}


def main() -> None:
    data = json.loads(SRC.read_text())["data"][158:316]
    results = []
    dropped = []
    for s in data:
        sid = str(s["meta"]["sent_id"])
        text = s["text"]
        ents = []
        for surface, label in ANN.get(sid, []):
            idx = text.find(surface)
            if idx == -1:
                dropped.append((sid, surface, label))
                continue
            multi = text.count(surface) > 1
            ents.append({
                "text": surface,
                "label": label,
                "start": idx,
                "end": idx + len(surface),
                "multi": multi,
            })
        results.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2))

    counts = {}
    for r in results:
        for e in r["entities"]:
            counts[e["label"]] = counts.get(e["label"], 0) + 1
    print("WROTE:", OUT)
    print("SENTENCES:", len(results))
    print("COUNTS:", counts)
    print("DROPPED:", dropped if dropped else "none")


if __name__ == "__main__":
    main()
