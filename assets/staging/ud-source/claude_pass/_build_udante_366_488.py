#!/usr/bin/env python3
"""Build NER JSON for UDante test data[366:488]. Offsets computed deterministically."""
import json
import os

SRC = os.path.join(os.path.dirname(__file__), "..", "ud-udante-test.json")
OUT = os.path.join(os.path.dirname(__file__), "udante_366_488.json")

# Manually decided (surface, label) pairs per sent_id. Surfaces copied exactly from text.
ANNO = {
    "DVE-270": [("Oratius", "PERSON")],
    "DVE-285": [("latii", "LOC")],  # genitive of Latium (region)
    "DVE-287-a": [("Gerardus", "PERSON")],
    "DVE-287-d": [("Nauarre", "LOC")],  # Navarre
    "DVE-287-e": [("Guido Guinizelli", "PERSON")],
    "DVE-287-f": [("Columpnis", "PERSON"), ("Messana", "LOC")],
    "DVE-287-g": [("Renaldus", "PERSON"), ("Aquino", "LOC")],
    "DVE-287-h": [("Cynus", "PERSON"), ("Pistoriensis", "NORP")],
    "DVE-297": [("Aristotiles", "PERSON"), ("Alexandri", "PERSON")],
    "DVE-304-a": [("Petrus", "PERSON"), ("Bertam", "PERSON")],
    "DVE-304-d": [("Florentia", "LOC"), ("Trinacriam", "LOC"), ("Totila", "PERSON")],
    "DVE-306-a": [("Gerardus", "PERSON")],
    "DVE-306-b": [("Folquetus", "PERSON"), ("Marsilia", "LOC")],
    "DVE-306-c": [("Arnaldus Danielis", "PERSON")],
    "DVE-306-d": [("Namericus", "PERSON"), ("Belnui", "LOC")],
    "DVE-306-e": [("Namericus", "PERSON"), ("Peculiano", "LOC")],
    "DVE-306-f": [("Nauarre", "LOC")],
    "DVE-306-g": [("Messana", "LOC")],
    "DVE-306-h": [("Guido Guinizelli", "PERSON")],
    "DVE-306-i": [("Guido Caualcantis", "PERSON")],
    "DVE-306-j": [("Cynus", "PERSON"), ("Pistorio", "LOC")],
    "DVE-308": [
        ("Uirgilium", "PERSON"), ("Ouidium", "PERSON"), ("Statium", "PERSON"),
        ("Lucanum", "PERSON"), ("Titum Liuium", "PERSON"), ("Plinium", "PERSON"),
        ("Frontinum", "PERSON"), ("Paulum Orosium", "PERSON"),
    ],
    "DVE-309": [("Guictonem", "PERSON"), ("Aretinum", "NORP")],
    "DVE-330-a": [("Uirgilius", "PERSON")],
}


def main():
    d = json.load(open(SRC))
    seg = d["data"][366:488]
    out = []
    dropped = []
    for s in seg:
        sid = s["meta"].get("sent_id")
        text = s["text"]
        ents = []
        for surf, label in ANNO.get(sid, []):
            idx = text.find(surf)
            if idx == -1:
                dropped.append((sid, surf, label))
                continue
            multi = text.count(surf) > 1
            ents.append({
                "text": surf,
                "label": label,
                "start": idx,
                "end": idx + len(surf),
                "multi": multi,
            })
        out.append({"sent_id": sid, "text": text, "entities": ents})

    with open(OUT, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # Report
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}
    for o in out:
        for e in o["entities"]:
            counts[e["label"]] += 1
    print("WROTE:", os.path.abspath(OUT))
    print("SENTENCES:", len(out))
    print("COUNTS:", counts)
    print("TOTAL ENTITIES:", sum(counts.values()))
    if dropped:
        print("DROPPED:")
        for sid, surf, label in dropped:
            print("  - %s %r (%s): not an exact substring" % (sid, surf, label))
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
