import json

SRC = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-perseus-test.json"
OUT = "/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/perseus_118_236.json"

d = json.load(open(SRC))
data = d["data"]
sl = data[118:236]

# Annotations keyed by sent_id -> list of (surface, label)
ann = {
    "phi0959.phi006.perseus-lat1.tb.xml@94": [("Parnasus", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@98": [("Tritona", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@105": [],
    "phi0959.phi006.perseus-lat1.tb.xml@106": [],
    "phi0959.phi006.perseus-lat1.tb.xml@107": [],
    "phi0959.phi006.perseus-lat1.tb.xml@109": [],
    "phi0959.phi006.perseus-lat1.tb.xml@110": [],
    "phi0959.phi006.perseus-lat1.tb.xml@112": [],
    "phi0959.phi006.perseus-lat1.tb.xml@114": [],
    "phi0959.phi006.perseus-lat1.tb.xml@115": [],
    "phi0959.phi006.perseus-lat1.tb.xml@117": [("Cephisidas", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@118": [],
    "phi0959.phi006.perseus-lat1.tb.xml@119": [("Themi", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@122": [("Pyrrha", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@123": [],
    "phi0959.phi006.perseus-lat1.tb.xml@125": [],
    "phi0959.phi006.perseus-lat1.tb.xml@128": [],
    "phi0959.phi006.perseus-lat1.tb.xml@129": [],
    "phi0959.phi006.perseus-lat1.tb.xml@130": [],
    "phi0959.phi006.perseus-lat1.tb.xml@135": [],
    "phi0959.phi006.perseus-lat1.tb.xml@136": [],
    "phi0959.phi006.perseus-lat1.tb.xml@140": [("Nilus", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@142": [],
    "phi0959.phi006.perseus-lat1.tb.xml@143": [],
    "phi0959.phi006.perseus-lat1.tb.xml@145": [("Python", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@146": [],
    "phi0959.phi006.perseus-lat1.tb.xml@147": [],
    "phi0959.phi006.perseus-lat1.tb.xml@148": [],  # "Pythia" = the Pythian Games (event/institution) -> not tagged
    "phi0959.phi006.perseus-lat1.tb.xml@149": [],
    "phi0959.phi006.perseus-lat1.tb.xml@153": [("Pythona", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@157": [("Parnasi", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@158": [],
    "phi0959.phi006.perseus-lat1.tb.xml@159": [],
    "phi0959.phi006.perseus-lat1.tb.xml@162": [("Phoebes", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@163": [],
    "phi0959.phi006.perseus-lat1.tb.xml@166": [],
    "phi0959.phi006.perseus-lat1.tb.xml@169": [],
    "phi0959.phi006.perseus-lat1.tb.xml@170": [("Phoebus", "PERSON"), ("Daphnes", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@173": [],
    "phi0959.phi006.perseus-lat1.tb.xml@174": [],
    "phi0959.phi006.perseus-lat1.tb.xml@175": [],
    "phi0959.phi006.perseus-lat1.tb.xml@177": [],
    "phi0959.phi006.perseus-lat1.tb.xml@179": [],
    "phi0959.phi006.perseus-lat1.tb.xml@180": [],
    "phi0959.phi006.perseus-lat1.tb.xml@182": [],
    "phi0959.phi006.perseus-lat1.tb.xml@185": [],
    "phi0959.phi006.perseus-lat1.tb.xml@186": [],
    "phi0959.phi006.perseus-lat1.tb.xml@187": [],
    "phi0959.phi006.perseus-lat1.tb.xml@188": [],
    "phi0959.phi006.perseus-lat1.tb.xml@190": [],
    "phi0959.phi006.perseus-lat1.tb.xml@191": [("Delphica", "LOC"), ("Claros", "LOC"), ("Tenedos", "LOC"), ("Patarea", "LOC"), ("Iuppiter", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@193": [],
    "phi0959.phi006.perseus-lat1.tb.xml@195": [],
    "phi0959.phi006.perseus-lat1.tb.xml@197": [("Peneia", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@202": [("Amoris", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@203": [("Peneidas", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@205": [],
    "phi0959.phi006.perseus-lat1.tb.xml@207": [],
    "phi0959.phi006.perseus-lat1.tb.xml@208": [("Phoebus", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@209": [],
    "phi0959.phi006.perseus-lat1.tb.xml@210": [],
    "phi0959.phi006.perseus-lat1.tb.xml@212": [("Latiis", "NORP")],
    "phi0959.phi006.perseus-lat1.tb.xml@214": [("Paean", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@217": [("Tempe", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@218": [("Peneus", "PERSON"), ("Pindo", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@221": [("Sperchios", "LOC"), ("Enipeus", "LOC"), ("Apidanus", "LOC"), ("Amphrysos", "LOC"), ("Aeas", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@224": [],
    "phi0959.phi006.perseus-lat1.tb.xml@226": [("Iuppiter", "PERSON"), ("Ioue", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@230": [("Lernae", "LOC"), ("Lyrcea", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@233": [],
    "phi0959.phi006.perseus-lat1.tb.xml@234": [("Inachidos", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@235": [],
    "phi0959.phi006.perseus-lat1.tb.xml@237": [("Saturnia", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@238": [],
    "phi0959.phi006.perseus-lat1.tb.xml@240": [],
    "phi0959.phi006.perseus-lat1.tb.xml@246": [("Io", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@247": [("Io", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@248": [],
    "phi0959.phi006.perseus-lat1.tb.xml@249": [],
    "phi0959.phi006.perseus-lat1.tb.xml@250": [],
    "phi0959.phi006.perseus-lat1.tb.xml@252": [("Inachidas", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@253": [],
    "phi0959.phi006.perseus-lat1.tb.xml@255": [],
    "phi0959.phi006.perseus-lat1.tb.xml@256": [("Inachus", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@258": [],
    "phi0959.phi006.perseus-lat1.tb.xml@261": [],
    "phi0959.phi006.perseus-lat1.tb.xml@262": [],
    "phi0959.phi006.perseus-lat1.tb.xml@263": [],
    "phi0959.phi006.perseus-lat1.tb.xml@267": [("Argus", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@268": [],
    "phi0959.phi006.perseus-lat1.tb.xml@271": [("Ioue", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@273": [],
    "phi0959.phi006.perseus-lat1.tb.xml@275": [("Atlantiades", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@279": [("Syringa", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@280": [],
    "phi0959.phi006.perseus-lat1.tb.xml@281": [("Ortygiam", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@283": [],
    "phi0959.phi006.perseus-lat1.tb.xml@285": [("Pana", "PERSON"), ("Syringa", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@286": [],
    "phi0959.phi006.perseus-lat1.tb.xml@288": [],
    "phi0959.phi006.perseus-lat1.tb.xml@289": [("Cyllenius", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@290": [],
    "phi0959.phi006.perseus-lat1.tb.xml@293": [("Saturnia", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@294": [("Erinyn", "PERSON"), ("Argolicae", "NORP")],
    "phi0959.phi006.perseus-lat1.tb.xml@295": [("Nile", "LOC")],
    "phi0959.phi006.perseus-lat1.tb.xml@296": [("Ioue", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@297": [],
    "phi0959.phi006.perseus-lat1.tb.xml@299": [],
    "phi0959.phi006.perseus-lat1.tb.xml@301": [],
    "phi0959.phi006.perseus-lat1.tb.xml@302": [],
    "phi0959.phi006.perseus-lat1.tb.xml@303": [],
    "phi0959.phi006.perseus-lat1.tb.xml@305": [("Sole", "PERSON"), ("Phaethon", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@309": [],
    "phi0959.phi006.perseus-lat1.tb.xml@311": [("Meropis", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@312": [("Clymene", "PERSON"), ("Phaethontis", "PERSON"), ("Sole", "PERSON")],
    "phi0959.phi006.perseus-lat1.tb.xml@313": [],
    "phi0959.phi006.perseus-lat1.tb.xml@315": [],
    "phi0959.phi006.perseus-lat1.tb.xml@317": [("Phaethon", "PERSON"), ("Aethiopas", "NORP"), ("Indos", "NORP")],
}

records = []
dropped = []
for s in sl:
    sid = s["meta"]["sent_id"]
    text = s["text"]
    ents = []
    for surface, label in ann.get(sid, []):
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
    records.append({"sent_id": sid, "text": text, "entities": ents})

with open(OUT, "w") as f:
    f.write(json.dumps(records, ensure_ascii=False, indent=2))

from collections import Counter
c = Counter()
for r in records:
    for e in r["entities"]:
        c[e["label"]] += 1
print("WROTE", OUT)
print("SENTENCES", len(records))
print("COUNTS", dict(c))
print("TOTAL_ENTITIES", sum(c.values()))
print("DROPPED", dropped)
