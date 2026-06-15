#!/usr/bin/env python3
"""Deterministic offset builder for PROIEL test slice [632:790].

Reads annotation (surface, label) decisions made by hand against the
ANNOTATION_RULES.md (PERSON / LOC / NORP), computes char offsets via
str.find (first occurrence default; multi:true when >1 occurrence;
DROP + log any surface that is not an exact substring of the sentence).
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/proiel_632_790.json")

# (surface, label) decisions per sent_id. Surfaces copied EXACTLY from text.
ANNOTATIONS: dict[str, list[tuple[str, str]]] = {
    # Romans 2 (Vulgate NT)
    "26606": [("Iudaeus", "NORP")],
    "26608": [("Iudaeus", "NORP")],
    # Revelation 2-3 (Vulgate NT)
    "33551": [("Sardis", "LOC")],
    "33558": [("Sardis", "LOC")],
    "33562": [("Philadelphiae", "LOC")],
    "33563": [("Dauid", "PERSON")],
    "33569": [("Satanae", "PERSON"), ("Iudaeos", "NORP")],
    "33575": [("Hierusalem", "LOC")],
    "33577": [("Laodiciae", "LOC")],
    # Revelation 5
    "33623": [("Iuda", "NORP"), ("Dauid", "PERSON")],
    # Palladius/agronomic text
    "159880": [("gallici", "NORP")],
}


def build():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"]
    sl = data[632:790]

    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for s in sl:
        sid = s["meta"]["sent_id"]
        text = s["text"]
        ents = []
        for surface, label in ANNOTATIONS.get(sid, []):
            idx = text.find(surface)
            if idx == -1:
                dropped.append((sid, surface, label, "not a substring"))
                continue
            multi = text.count(surface) > 1
            ents.append({
                "text": surface,
                "label": label,
                "start": idx,
                "end": idx + len(surface),
                "multi": multi,
            })
            counts[label] += 1
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    print(f"TOTAL ENTITIES: {sum(counts.values())}")
    if dropped:
        print("DROPPED:")
        for row in dropped:
            print("  ", row)
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    build()
