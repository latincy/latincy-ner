import json

SRC = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-perseus-test.json"
OUT = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/perseus_472_590.json"

with open(SRC) as f:
    d = json.load(f)
data = d["data"]
sl = data[472:590]

# Manual annotations keyed by sent_id -> list of (surface, label)
ann = {
    "phi0972.phi001.perseus-lat1.xml@492": [("Iouis", "PERSON"), ("Caesar", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@495": [("Caesar", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@499": [("Cassandra", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@500": [("Mummius", "PERSON"), ("Daedalus", "PERSON"),
                                            ("Niobam", "PERSON"), ("Troianum", "NORP")],
    "phi0972.phi001.perseus-lat1.xml@516": [("Syrum", "NORP")],
    "phi0972.phi001.perseus-lat1.xml@518": [("Fortunata", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@537": [("Trimalchio", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@538": [("Baias", "LOC")],
    "phi0972.phi001.perseus-lat1.xml@542": [("Trimalchio", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@559": [("Fortuna", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@580": [("Ioue", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@592": [("Atticum", "NORP")],
    "phi0972.phi001.perseus-lat1.xml@612": [("Romanus", "NORP")],
    "phi0972.phi001.perseus-lat1.xml@647": [("Giton", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@649": [("Saturnalia", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@696": [("Trimalchio", "PERSON"), ("Homeristae", "NORP"),
                                            ("Graecis", "NORP")],
    "phi0972.phi001.perseus-lat1.xml@698": [("Diomedes", "PERSON"), ("Ganymedes", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@699": [("Helena", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@700": [("Agamemnon", "PERSON"), ("Dianae", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@701": [("Homeros", "PERSON"), ("Troiani", "NORP"),
                                            ("Parentini", "NORP")],
    "phi0972.phi001.perseus-lat1.xml@702": [("Iphigeniam", "PERSON"), ("Achilli", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@719": [("Trimalchionis", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@731": [("Gauillae", "PERSON")],
    "phi0972.phi001.perseus-lat1.xml@732": [("Terentii", "PERSON")],
}

out = []
dropped = []
counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

for s in sl:
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
        counts[label] += 1
    out.append({"sent_id": sid, "text": text, "entities": ents})

with open(OUT, "w") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=2))

print("WROTE", OUT)
print("SENTENCES", len(out))
print("COUNTS", counts)
print("DROPPED", len(dropped))
for w in dropped:
    print("  DROP", w)
