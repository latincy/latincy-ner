import json
import os

SRC = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-perseus-test.json"
OUT = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/perseus_354_472.json"

d = json.load(open(SRC))
data = d["data"]
sl = data[354:472]

# sent_id (last @NNN segment) -> list of (surface, label)
ANN = {
    "242": [],
    "287": [("Phileros", "PERSON"), ("Ganymedes", "PERSON")],
    "336": [("Titus", "PERSON")],
    "319": [("Iouem", "PERSON")],
    "345": [("Glyco", "PERSON")],
    "350": [("Glyco", "PERSON"), ("Hermogenis", "PERSON")],
    "353": [("Glyco", "PERSON")],  # appears twice -> multi
    "354": [("Orcus", "PERSON")],
    "357": [("Norbano", "PERSON")],
    "371": [("Agamemnon", "PERSON")],
    "394": [("Orcus", "PERSON")],
    "397": [("Phileronem", "PERSON")],
    "399": [("Norbanum", "PERSON")],
    "401": [("Trimalchio", "PERSON")],
    "409": [("Iouis", "PERSON")],
    "410": [("Fortunata", "PERSON")],
    "431": [("Tarraciniensibus", "NORP"), ("Tarentinis", "NORP")],
    "432": [("Siciliam", "LOC"), ("Africam", "LOC")],
    "435": [("Graecam", "NORP"), ("Latinam", "NORP")],
    "443": [("Homerum", "PERSON")],
    "470": [("Agamemnon", "PERSON"), ("Trimalchio", "PERSON")],
    "472": [("Corintho", "LOC")],
}


def key(sent_id):
    return sent_id.rsplit("@", 1)[-1]


out = []
dropped = []
counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

for s in sl:
    sid = s["meta"]["sent_id"]
    text = s["text"]
    k = key(sid)
    ents = []
    for surface, label in ANN.get(k, []):
        idx = text.find(surface)
        if idx == -1:
            dropped.append((sid, surface, label, "not an exact substring"))
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

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=2))

print("WROTE:", OUT)
print("sentences processed:", len(out))
print("counts:", counts)
print("total entities:", sum(counts.values()))
print("dropped:")
for row in dropped:
    print("  ", row)
