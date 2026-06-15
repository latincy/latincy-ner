import json

SRC = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-perseus-test.json"
OUT = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/perseus_590_708.json"

# (sent_id_suffix, [(surface, label), ...])
ANN = {
    "@756": [("Melissa", "PERSON")],
    "@769": [("Chiam", "NORP")],
    "@793": [("Graecum", "NORP")],
    "@800": [("Croesi", "PERSON")],
    "@802": [("Trimalchio", "PERSON")],
    "@805": [("Trimalchio", "PERSON")],
    "@816": [("Habinnam", "PERSON")],
    "@822": [("Scissa", "PERSON")],
    "@836": [("Scintilla", "PERSON")],
    "@839": [("Palamedes", "PERSON")],
    "@864": [("Scintillae", "PERSON")],
    "@865": [("Trimalchio", "PERSON")],
    "@869": [("Alexandrinus", "NORP"), ("Trimalchione", "PERSON")],
    "@872": [("Habinnae", "PERSON")],
    "@879": [("Musae", "PERSON")],
    "@883": [("Uenus", "PERSON")],
    "@905": [("Trimalchio", "PERSON")],
    "@916": [("Trimalchio", "PERSON")],
    "@931": [("Philargyro", "PERSON"), ("Carioni", "PERSON")],
    "@937": [("Petraitis", "PERSON")],
    "@950": [("Fortunatae", "PERSON")],
    "@958": [("Romae", "LOC")],
    "@962": [("Trimalchio", "PERSON")],
    "@963": [("Fortunata", "PERSON"), ("Habinnas", "PERSON")],
    "@971": [("Gitone", "PERSON"), ("Ascyltos", "PERSON")],
    "@974": [("Giton", "PERSON")],
    "@981": [("Giton", "PERSON"), ("Trimalchio", "PERSON")],
    "@983": [("Menecratis", "PERSON")],
    "@986": [("Trimalchioni", "PERSON")],
}

with open(SRC) as f:
    d = json.load(f)
data = d["data"][590:708]

out = []
dropped = []
for s in data:
    sid = s["meta"]["sent_id"]
    text = s["text"]
    suffix = "@" + sid.split("@")[-1]
    ents = []
    for surface, label in ANN.get(suffix, []):
        start = text.find(surface)
        if start == -1:
            dropped.append((sid, surface, label))
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

with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# report
counts = {"PERSON": 0, "LOC": 0, "NORP": 0}
for rec in out:
    for e in rec["entities"]:
        counts[e["label"]] += 1
print("WROTE:", OUT)
print("SENTENCES:", len(out))
print("COUNTS:", counts)
print("TOTAL ENTITIES:", sum(counts.values()))
print("DROPPED:", dropped)
