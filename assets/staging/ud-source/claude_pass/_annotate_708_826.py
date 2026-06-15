import json
import os

SRC = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-perseus-test.json"
OUT = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/perseus_708_826.json"

with open(SRC) as f:
    d = json.load(f)
data = d["data"][708:826]

# sent_id -> list of (surface, label)
ann = {
    "phi0972.phi001.perseus-lat1.xml@992": [("Trimalchio", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@999": [("Daedalus", "PERSON"), ("Fortunata", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1006": [("Trimalchioni", "PERSON"), ("Fortunata", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1009": [("Trimalchio", "PERSON"), ("Fortunatae", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1012": [("Fortunata", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1023": [("Habinna", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1027": [("Scintilla", "PERSON"), ("Gaium", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1033": [("Fortunata", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1058": [("Caesari", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1064": [("Neptunus", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1070": [("Fortunata", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1094": [("Apuliae", "LOC")],
    "phi0972.phi001.perseus-lat1.xml@1095": [("Mercurius", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1107": [("Stiche", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@1120": [("Agamemnoni", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@1": [("Aesopus", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@22": [("Ioue", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@29": [("Mercurio", "PERSON"), ("Iouem", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@53": [("Aesopus", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@54": [("Sol", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@55": [("Iuppiter", "PERSON")],
}

dropped = []
out = []
for s in data:
    sid = s["meta"]["sent_id"]
    text = s["text"]
    ents = []
    for surface, label in ann.get(sid, []):
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
    out.append({"sent_id": sid, "text": text, "entities": ents})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=2))

from collections import Counter
c = Counter(e["label"] for r in out for e in r["entities"])
print("written:", OUT)
print("sentences:", len(out))
print("counts:", dict(c))
print("total entities:", sum(c.values()))
print("dropped:", dropped)
