#!/usr/bin/env python3
"""Build NER annotations for PROIEL test slice data[790:948].

Offsets computed deterministically with str.find (first occurrence default).
multi=True when a surface occurs more than once. Non-substring surfaces are
dropped and logged.
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/proiel_790_948.json")

# (surface, label) pairs per sent_id, surfaces copied exactly from text.
ANN: dict[str, list[tuple[str, str]]] = {
    "82318": [("Marco Cornelio", "PERSON"), ("Tribus Tabernis", "LOC")],
    "82319": [("Canusinus", "NORP")],
    "76046": [("Epirum", "LOC")],
    "76047": [("Amaltheam", "LOC"), ("Sicyonem", "LOC"),
              ("Antonium", "PERSON"), ("Epiro", "LOC")],
    "76048": [("Achaicis", "NORP"), ("Epiroticis", "NORP")],
    "76050": [("Allobrogum", "NORP")],
    "82332": [("Lycurgei", "NORP")],
    "76052": [("Catulus", "PERSON")],
    "82321": [("Hortensius", "PERSON")],
    "76057": [("Caesarem", "PERSON"), ("Quinto Cornificio", "PERSON")],
    "82330": [("Caesarem", "PERSON")],
    "76058": [("Piso", "PERSON"), ("Publi Clodi", "PERSON")],
    "76059": [("Messalla", "PERSON")],
    "76060": [("Clodi", "PERSON")],
    "82333": [("Cato", "PERSON")],
    "76069": [("Miseni", "LOC"), ("Puteolorum", "LOC")],
    "76081": [("Teucris", "PERSON")],
    "76084": [("Marco Messalla", "PERSON"), ("Marco Pisone", "PERSON")],
    "76086": [("Pompei", "PERSON")],
    "76087": [("Pisonis", "PERSON"), ("Fufius", "PERSON"),
              ("Pompeium", "PERSON")],
    "76092": [("Pompeius", "PERSON")],
    "76093": [("Messalla", "PERSON"), ("Pompeio", "PERSON")],
    "76095": [("Crassus", "PERSON")],
    "76097": [("Aristarchus", "PERSON")],
    "76098": [("Pompeium", "PERSON")],
    "76099": [("Crassum", "PERSON")],
    "76100": [("Crasso", "PERSON")],
    "76101": [("Pompeio", "PERSON")],
    "76106": [("Italiae", "LOC")],
    "76109": [("Romanae", "NORP")],
    "76111": [("Catilinae", "PERSON"), ("Curionis", "PERSON")],
    "76112": [("Piso", "PERSON")],
    "76114": [("Cato", "PERSON")],
    "82354": [("Pisoni", "PERSON")],
    "76115": [("Hortensius", "PERSON")],
    "82355": [("Fauoni", "PERSON")],
    "76117": [("Pisone", "PERSON"), ("Clodio", "PERSON"),
              ("Curioni", "PERSON")],
    "76119": [("Fufius", "PERSON")],
    "76120": [("Clodius", "PERSON"), ("Lucullum", "PERSON"),
              ("Hortensium", "PERSON"), ("Gaium Pisonem", "PERSON"),
              ("Messallam", "PERSON")],
    "76122": [("Romanas", "NORP")],
    "76124": [("Messalla", "PERSON")],
    "76125": [("Pompeium", "PERSON")],
    "76127": [("Clodi", "PERSON")],
    "76128": [("Fufium", "PERSON")],
    "76129": [("Cornuto", "PERSON"), ("Pseudocatone", "PERSON")],
    "76132": [("Τεῦκρις", "PERSON")],
    "76134": [("Quintus", "PERSON"), ("Tusculanum", "LOC")],
    "76135": [("Lucceio", "PERSON")],
}


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))["data"][790:948]
    by_id = {s["meta"]["sent_id"]: s["text"] for s in data}

    out = []
    dropped = []
    for s in data:
        sid = s["meta"]["sent_id"]
        text = s["text"]
        ents = []
        for surface, label in ANN.get(sid, []):
            idx = text.find(surface)
            if idx == -1:
                dropped.append((sid, surface, label))
                continue
            ent = {
                "text": surface,
                "label": label,
                "start": idx,
                "end": idx + len(surface),
            }
            if text.count(surface) > 1:
                ent["multi"] = True
            ents.append(ent)
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    counts: dict[str, int] = {}
    for rec in out:
        for e in rec["entities"]:
            counts[e["label"]] = counts.get(e["label"], 0) + 1

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    print(f"TOTAL ENTITIES: {sum(counts.values())}")
    if dropped:
        print("DROPPED:")
        for sid, surf, lab in dropped:
            print(f"  {sid} {lab} {surf!r}")
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
