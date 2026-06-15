#!/usr/bin/env python3
"""Build NER annotations for PROIEL test data[0:158] (Matthew 6 + Mark 6).

Deterministic offset computation: str.find (first occurrence default),
multi=True if surface occurs >1 time; drop+log any non-substring surface.
"""
import json
from pathlib import Path

SRC = Path("/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/proiel_0_158.json")

# (data-index, surface, label) pairs — surfaces copied exactly from text.
ANNOTATIONS: dict[int, list[tuple[str, str]]] = {
    11: [("ethnici", "NORP")],          # like the heathen / gentiles
    47: [("Salomon", "PERSON")],
    51: [("gentes", "NORP")],           # the Gentiles/nations seek these things
    64: [("Mariae", "PERSON"), ("Iacobi", "PERSON"), ("Ioseph", "PERSON"),
         ("Iudae", "PERSON"), ("Simonis", "PERSON")],
    67: [("Iesus", "PERSON")],
    79: [("Herodes", "PERSON")],        # exclude title 'rex'
    80: [("Iohannes", "PERSON")],       # exclude appellative 'Baptista'
    83: [("Helias", "PERSON")],
    86: [("Herodes", "PERSON")],
    87: [("Iohannem", "PERSON")],
    88: [("Herodes", "PERSON"), ("Iohannem", "PERSON"), ("Herodiadem", "PERSON"),
         ("Philippi", "PERSON")],
    89: [("Iohannes", "PERSON"), ("Herodi", "PERSON")],
    91: [("Herodias", "PERSON")],
    93: [("Herodes", "PERSON"), ("Iohannem", "PERSON")],
    95: [("Herodes", "PERSON"), ("Galilaeae", "LOC")],
    96: [("Herodiadis", "PERSON"), ("Herodi", "PERSON")],
    103: [("Iohannis", "PERSON")],      # exclude appellative 'Baptistae'
    105: [("Iohannis", "PERSON")],      # exclude appellative 'Baptistae'
    112: [("Iesum", "PERSON")],
    120: [("Iesus", "PERSON")],
    141: [("Bethsaidam", "LOC")],
    156: [("Gennesareth", "LOC")],      # terram Gennesareth -> place name
}


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"]
    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for i in range(158):
        rec = data[i]
        text = rec["text"]
        sent_id = rec["meta"]["sent_id"]
        ents = []
        for surface, label in ANNOTATIONS.get(i, []):
            start = text.find(surface)
            if start == -1:
                dropped.append((i, sent_id, surface, label))
                continue
            multi = text.count(surface) > 1
            ents.append({
                "text": surface,
                "label": label,
                "start": start,
                "end": start + len(surface),
                "multi": multi,
            })
            counts[label] += 1
        out.append({"sent_id": sent_id, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    print(f"TOTAL ENTITIES: {sum(counts.values())}")
    if dropped:
        print("DROPPED (non-substring surfaces):")
        for i, sid, surf, lab in dropped:
            print(f"  [{i}] sent_id={sid} surface={surf!r} label={lab}")
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
