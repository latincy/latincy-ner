import json
from pathlib import Path

SRC = Path("/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/ud-perseus-test.json")
OUT = Path("/Volumes/fiona/work/code/diy/latincy-v3/latincy-ner/assets/staging/ud-source/claude_pass/perseus_826_939.json")

d = json.load(open(SRC))
data = d["data"]
sl = data[826:939]

# Manual annotations keyed by sent_id: list of (surface, label)
ann = {
    "phi0975.phi001.perseus-lat1.tb.xml@77": [("Aesopi", "PERSON")],
    "phi0975.phi001.perseus-lat1.tb.xml@221": [("Aesopi", "PERSON")],
}

out = []
dropped = []
for s in sl:
    sid = s["meta"]["sent_id"]
    text = s["text"]
    ents = []
    for surface, label in ann.get(sid, []):
        idx = text.find(surface)
        if idx == -1:
            dropped.append((sid, surface, label, "not a substring"))
            continue
        count = text.count(surface)
        ents.append({
            "text": surface,
            "label": label,
            "start": idx,
            "end": idx + len(surface),
            "multi": count > 1,
        })
    out.append({"sent_id": sid, "text": text, "entities": ents})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2))

# Report
from collections import Counter
c = Counter()
for r in out:
    for e in r["entities"]:
        c[e["label"]] += 1
print("WROTE", OUT)
print("SENTENCES", len(out))
print("COUNTS", dict(c))
print("DROPPED", dropped)
