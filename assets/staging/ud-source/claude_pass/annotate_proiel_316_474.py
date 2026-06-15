#!/usr/bin/env python3
"""Deterministic offset computation for PROIEL test slice [316:474]."""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/proiel_316_474.json")

# Annotations: sent_id -> list of (surface, label) copied EXACTLY from text.
ANN = {
    "17669": [("Abraham", "PERSON")],
    "17672": [("Mosen", "PERSON")],
    "18765": [("Iesus", "PERSON"), ("Galilaeae", "LOC"), ("Tiberiadis", "LOC")],
    "18767": [("Iesus", "PERSON")],
    "18768": [("Iudaeorum", "NORP")],
    "18769": [("Iesus", "PERSON"), ("Philippum", "PERSON")],
    "18773": [("Philippus", "PERSON")],
    "18775": [("Andreas", "PERSON"), ("Simonis Petri", "PERSON")],
    "18778": [("Iesus", "PERSON")],
    "18782": [("Iesus", "PERSON")],
    "18790": [("Iesus", "PERSON")],
    "18792": [("Capharnaum", "LOC")],
    "18793": [("Iesus", "PERSON")],
    "18795": [("Iesum", "PERSON")],
    "18799": [("Iesus", "PERSON")],
    "18800": [("Tiberiade", "LOC")],
    "18801": [("Iesus", "PERSON"), ("Capharnaum", "LOC"), ("Iesum", "PERSON")],
    "18804": [("Iesus", "PERSON")],
    "18811": [("Iesus", "PERSON")],
    "18818": [("Iesus", "PERSON")],
    "18820": [("Moses", "PERSON")],
    "18824": [("Iesus", "PERSON")],
    "18835": [("Iudaei", "NORP")],
    "18837": [("Iesus", "PERSON"), ("Ioseph", "PERSON")],
    "18840": [("Iesus", "PERSON")],
    "18856": [("Iudaei", "NORP")],
    "18858": [("Iesus", "PERSON")],
    "18870": [("Capharnaum", "LOC")],
    "18873": [("Iesus", "PERSON")],
    "18880": [("Iesus", "PERSON")],
    "18885": [("Iesus", "PERSON")],
    "18887": [("Simon Petrus", "PERSON")],
    "18890": [("Christus", "PERSON")],
    "18891": [("Iesus", "PERSON")],
    "18894": [("Iudam Simonis Scariotis", "PERSON")],
    "23714": [("Abraham", "PERSON"), ("Mesopotamiam", "LOC"), ("Charram", "LOC")],
    "23716": [("Chaldeorum", "NORP"), ("Charram", "LOC")],
    "23725": [("Isaac", "PERSON")],
    "23726": [("Isaac", "PERSON"), ("Iacob", "PERSON")],
    "23727": [("Iacob", "PERSON")],
    "23728": [("Ioseph", "PERSON"), ("Aegyptum", "LOC")],
    "23729": [("Pharaonis", "PERSON"), ("Aegypti", "LOC")],
    "23730": [("Aegyptum", "LOC")],
    "23733": [("Iacob", "PERSON"), ("Aegypto", "LOC")],
    "23734": [("Ioseph", "PERSON"), ("Pharaoni", "PERSON")],
    "23735": [("Ioseph", "PERSON"), ("Iacob", "PERSON")],
    "23736": [("Iacob", "PERSON"), ("Aegyptum", "LOC")],
}

data = json.load(open(SRC))["data"][316:474]
sub = {s["meta"]["sent_id"]: s["text"] for s in data}

out = []
dropped = []
for s in data:
    sid = s["meta"]["sent_id"]
    text = s["text"]
    ents = []
    for surface, label in ANN.get(sid, []):
        start = text.find(surface)
        if start == -1:
            dropped.append((sid, surface, label, "not a substring"))
            continue
        multi = text.count(surface) > 1
        ents.append({
            "text": surface,
            "label": label,
            "start": start,
            "end": start + len(surface),
            "multi": multi,
        })
    out.append({"sent_id": sid, "text": text, "entities": ents})

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# Report
from collections import Counter
c = Counter()
for o in out:
    for e in o["entities"]:
        c[e["label"]] += 1
print("WRITTEN:", OUT)
print("SENTENCES:", len(out))
print("COUNTS:", dict(c), "TOTAL", sum(c.values()))
print("DROPPED:", len(dropped))
for d in dropped:
    print("  DROP", d)
