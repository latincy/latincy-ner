import json
import os

SRC = "assets/staging/ud-source/ud-proiel-test.json"
OUT = "assets/staging/ud-source/claude_pass/proiel_948_1106.json"

# (sent_id -> list of (surface, label)) annotations, surfaces copied EXACTLY from text.
ANN = {
    "82358": [("Asiam", "LOC"), ("Quinto", "PERSON")],
    "76142": [("Quinto", "PERSON")],
    "82359": [("Brundisio", "LOC")],
    "76877": [("Anicato", "PERSON")],
    "76878": [("Numestium", "PERSON")],
    "76879": [("Caecilium", "PERSON")],
    "76880": [("Uarro", "PERSON")],
    "76881": [("Pompeius", "PERSON")],
    "76885": [("Clodius", "PERSON")],
    "76886": [("Pompeius", "PERSON")],
    "81808": [("Amalthea", "LOC")],
    "76894": [("Bibulus", "PERSON")],
    "76901": [("Bibulus", "PERSON")],
    "76899": [("Furio", "PERSON")],
    "81813": [("Laelium", "PERSON"), ("Atticum", "PERSON")],
    "76900": [("Diodotus", "PERSON")],
    "76902": [("Uibio", "PERSON")],
    "76907": [("Catoni", "PERSON")],
    "81818": [("Italiae", "LOC")],
    "76912": [("Bibuli", "PERSON")],
    "76914": [("Crasso", "PERSON")],
    "76915": [("Apelles", "PERSON"), ("Uenerem", "PERSON"), ("Protogenes", "PERSON"), ("Ialysum", "PERSON")],
    "76917": [("Bibuli", "PERSON")],
    "76918": [("Bibuli", "PERSON")],
    "76920": [("Caesar", "PERSON"), ("Bibulum", "PERSON")],
    "76924": [("Clodius", "PERSON")],
    "76925": [("Pompeius", "PERSON")],
    "76930": [("Uarro", "PERSON")],
    "76931": [("Pompeius", "PERSON")],
    "76933": [("Sicyoniis", "NORP")],
    "77268": [("Thessalonicae", "LOC")],
    "83575": [("Asiam", "LOC")],
    "77269": [("Epirum", "LOC")],
    "77272": [("Sesti", "PERSON"), ("Terentiae", "PERSON"), ("Tulliolae", "PERSON")],
    "77273": [("Epirus", "LOC")],
    "77274": [("Tite Pomponi", "PERSON"), ("Quintum", "PERSON"), ("Terentiam", "PERSON")],
    "77566": [("Quinto", "PERSON")],
    "77567": [("Chaerippus", "PERSON")],
    "77568": [("Apollonio", "PERSON"), ("Graeco", "NORP"), ("Romanis", "NORP")],
    "77570": [("Terentius", "PERSON")],
    "77571": [("Metello", "PERSON")],
    "77573": [("Publium", "PERSON")],
    "84868": [("Milonem", "PERSON")],
    "77576": [("Arpinatium", "NORP"), ("Laterio", "LOC")],
    "84870": [("Ciceronem", "PERSON")],
    "78278": [("Romae", "LOC")],
    "78279": [("Epirum", "LOC")],
    "78283": [("Romae", "LOC"), ("Epiro", "LOC"), ("Parthi", "NORP"), ("Euphraten", "LOC"),
              ("Pacoro", "PERSON"), ("Orodis", "PERSON"), ("Parthorum", "NORP")],
    "78284": [("Bibulus", "PERSON"), ("Syria", "LOC")],
    "85788": [("Cassius", "PERSON"), ("Antiochia", "LOC"), ("Cappadocia", "LOC"),
              ("Taurum", "LOC"), ("Cybistra", "LOC"), ("Cyrrhestica", "LOC"), ("Syriae", "LOC")],
    "85790": [("Romae", "LOC")],
    "78287": [("Pompeium", "PERSON")],
    "78289": [("Romae", "LOC")],
    "78291": [("Ciliciam", "LOC")],
    "78292": [("Deiotari", "PERSON")],
    "78294": [("Romanorum", "NORP")],
    "78298": [("Romae", "LOC")],
    "78306": [("Cicerones", "PERSON"), ("Deiotarum", "PERSON"), ("Rhodum", "LOC")],
    "78307": [("Romae", "LOC")],
    "85793": [("Epiro", "LOC")],
    "78308": [("Bruti", "PERSON")],
    "52850": [("Caesari", "PERSON")],
}

d = json.load(open(SRC))
seg = d["data"][948:1106]
by_id = {s["meta"]["sent_id"]: s["text"] for s in seg}

out = []
dropped = []
for s in seg:
    sid = s["meta"]["sent_id"]
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
    ents.sort(key=lambda e: e["start"])
    out.append({"sent_id": sid, "text": text, "entities": ents})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

from collections import Counter
c = Counter(e["label"] for o in out for e in o["entities"])
print("written:", OUT)
print("sentences:", len(out))
print("counts:", dict(c))
print("total entities:", sum(c.values()))
print("dropped:", dropped)
