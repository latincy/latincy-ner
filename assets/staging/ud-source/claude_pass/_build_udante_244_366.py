#!/usr/bin/env python3
"""Build NER annotations for UDante test slice data[244:366].

Deterministic offsets via str.find (first occurrence). multi=True if surface
occurs >1 time in sentence. Non-substring surfaces are dropped and logged.
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-udante-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/udante_244_366.json")

# Manual (surface, label) annotations keyed by sent_id.
ANN = {
    "DVE-180": [("Latio", "LOC"), ("latie", "NORP"), ("Latinorum", "NORP")],
    "DVE-181": [],
    "DVE-182": [],
    "DVE-183-a": [],
    "DVE-183-b": [("Seneca", "PERSON"), ("Numa Pompilius", "PERSON")],
    "DVE-184": [],
    "DVE-185": [("Latinorum", "NORP"), ("Cynus Pistoriensis", "PERSON")],
    "DVE-186": [],
    "DVE-187": [],
    "DVE-188": [],
    "DVE-189": [],
    "DVE-190": [],
    "DVE-191": [],
    "DVE-192": [],
    "DVE-193": [],
    "DVE-194": [],
    "DVE-195": [("ytalia", "NORP")],
    "DVE-196": [],
    "DVE-197": [],
    "DVE-198": [],
    "DVE-199": [("Ytali", "NORP")],
    "DVE-200-a": [],
    "DVE-200-b": [],
    "DVE-201-a": [],
    "DVE-201-b": [],
    "DVE-202-a": [],
    "DVE-202-b": [],
    "DVE-203": [("Ytalorum", "NORP")],
    "DVE-204": [("Ytalorum", "NORP")],
    "DVE-205": [],
    "DVE-206-a": [("Alamannie", "LOC"), ("Ytalia", "LOC")],
    "DVE-206-b": [],
    "DVE-207": [("Ytalos", "NORP")],
    "DVE-208": [("latium", "NORP")],
    "DVE-209-a": [("Cremone", "LOC"), ("Lombardie", "LOC")],
    "DVE-209-b": [("Lombardie", "LOC"), ("Ytalie", "LOC")],
    "DVE-209-c": [("Ytalie", "LOC")],
    "DVE-210": [("cremonense", "NORP"), ("lombardum", "NORP"),
                ("semilatium", "NORP"), ("Ytalie", "LOC"), ("latium", "NORP")],
    "DVE-211": [("Ytalia", "LOC"), ("Siculi", "NORP"), ("Apuli", "NORP"),
                ("Tusci", "NORP"), ("Romandioli", "NORP"), ("Lombardi", "NORP"),
                ("Marchie", "LOC")],
    "DVE-212": [],
    "DVE-213": [],
    "DVE-214": [("latium", "NORP")],
    "DVE-215": [],
    "DVE-216": [],
    "DVE-217": [],
    "DVE-218-a": [],
    "DVE-218-b": [],
    "DVE-218-c": [],
    "DVE-219": [],
    "DVE-220": [],
    "DVE-221-a": [],
    "DVE-221-b": [],
    "DVE-221-c": [],
    "DVE-222": [],
    "DVE-223-a": [],
    "DVE-223-b": [],
    "DVE-223-c": [],
    "DVE-224": [],
    "DVE-225": [],
    "DVE-226": [],
    "DVE-227-a": [],
    "DVE-227-b": [],
    "DVE-228": [],
    "DVE-229": [],
    "DVE-230-a": [],
    "DVE-230-b": [],
    "DVE-230-c": [],
    "DVE-231-a": [],
    "DVE-231-b": [],
    "DVE-232": [],
    "DVE-233-a": [],
    "DVE-233-b": [],
    "DVE-234": [],
    "DVE-235-a": [],
    "DVE-235-b": [],
    "DVE-236-a": [],
    "DVE-236-b": [],
    "DVE-237-a": [],
    "DVE-237-b": [],
    "DVE-238": [],
    "DVE-239": [],
    "DVE-240": [],
    "DVE-241": [],
    "DVE-242-a": [],
    "DVE-242-b": [],
    "DVE-242-c": [],
    "DVE-243-a": [],
    "DVE-243-b": [],
    "DVE-244": [],
    "DVE-245": [],
    "DVE-246": [],
    "DVE-247": [],
    "DVE-248": [],
    "DVE-249-a": [("Bertramum de Bornio", "PERSON"), ("Arnaldum Danielem", "PERSON"),
                  ("Gerardum de Bornello", "PERSON")],
    "DVE-249-b": [("Cynum Pistoriensem", "PERSON")],
    "DVE-250-a": [("Bertramus", "PERSON")],
    "DVE-250-b": [("Arnaldus", "PERSON")],
    "DVE-250-c": [("Gerardus", "PERSON")],
    "DVE-250-d": [("Cynus", "PERSON")],
    "DVE-250-e": [],
    "DVE-251": [("latium", "NORP")],
    "DVE-252": [],
    "DVE-253": [],
    "DVE-254": [],
    "DVE-255": [],
    "DVE-256": [],
    "DVE-257": [],
    "DVE-258-a": [],
    "DVE-258-b": [],
    "DVE-258-c": [],
    "DVE-259-a": [],
    "DVE-259-b": [],
    "DVE-259-c": [],
    "DVE-260-a": [],
    "DVE-260-b": [],
    "DVE-260-c": [],
    "DVE-261-a": [],
    "DVE-261-b": [],
    "DVE-262": [],
    "DVE-263-a": [],
    "DVE-263-b": [],
    "DVE-264": [],
}


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"][244:366]

    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for s in data:
        sid = s["meta"]["sent_id"]
        text = s["text"]
        pairs = ANN.get(sid, [])
        ents = []
        for surface, label in pairs:
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
            counts[label] += 1
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    if dropped:
        print("DROPPED:")
        for sid, surface, label in dropped:
            print(f"  {sid}: {surface!r} ({label}) not a substring")
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
