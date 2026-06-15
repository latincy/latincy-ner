#!/usr/bin/env python3
"""Deterministic offset computation for PROIEL test slice [474:632].

Entity (surface, label) decisions are hand-curated per ANNOTATION_RULES.md
(PERSON / LOC / NORP). Offsets computed via str.find (first occurrence default;
multi=True if surface occurs >1 time; non-substring surfaces DROPPED + logged).
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/proiel_474_632.json")

# sent_id -> list of (surface, label)
ANN = {
    "23738": [("Sychem", "LOC"), ("Abraham", "PERSON"), ("Emmor", "PERSON")],
    # "filii Sychem": Sychem here is a personal patronym (son of Sychem/Hamor's
    # father); but the first Sychem is the place (Shechem). Surface "Sychem"
    # occurs twice -> multi. Tag once as LOC (first occurrence = the place).
    "23739": [("Deus", None), ("Abrahae", "PERSON"), ("Aegypto", "LOC"),
              ("Ioseph", "PERSON")],
    "23741": [("Moses", "PERSON")],
    "23743": [("Pharaonis", "PERSON")],
    "23744": [("Moses", "PERSON"), ("Aegyptiorum", "NORP")],
    "23745": [("Israhel", "NORP")],
    # "filios Israhel" = sons of Israel = the people/Israelites -> NORP
    "23746": [("Aegyptio", "NORP")],
    # "percusso Aegyptio" = an Egyptian (the man) -> NORP demonym substantive
    "23755": [("Aegyptium", "NORP")],
    "23756": [("Moses", "PERSON")],
    "23757": [("Madiam", "LOC")],
    "23758": [("Sina", "LOC")],
    "23759": [("Moses", "PERSON")],
    "23761": [("Abraham", "PERSON"), ("Isaac", "PERSON"), ("Iacob", "PERSON")],
    "23762": [("Moses", "PERSON")],
    "23766": [("Aegypto", "LOC")],
    "23767": [("Aegyptum", "LOC")],
    "23768": [("Mosen", "PERSON")],
    "23771": [("Aegypti", "LOC"), ("Rubro mari", "LOC")],
    # Rubrum mare = Red Sea -> LOC
    "23772": [("Moses", "PERSON"), ("Israhel", "NORP")],
    "23776": [("Aegyptum", "LOC"), ("Aaron", "PERSON")],
    "23779": [("Moses", "PERSON"), ("Aegypti", "LOC")],
    "23785": [("Mosen", "PERSON")],
    "23786": [("Iesu", "PERSON"), ("Dauid", "PERSON"), ("Iacob", "PERSON")],
    # "cum Iesu" = with Joshua (Vulgate Iesus = Joshua here); Deo Iacob = God of Jacob
    "23787": [("Salomon", "PERSON")],
    "23801": [("Iesum", "PERSON")],
    "23803": [],
    "23806": [("Saulus", "PERSON")],
    "23807": [("Stephanum", "PERSON")],
    "23808": [("Iesu", "PERSON")],
    "23812": [("Saulus", "PERSON")],
    "23813": [("Hierosolymis", "LOC"), ("Iudaeae", "LOC"), ("Samariae", "LOC")],
    # regiones Iudaeae et Samariae = regions of Judaea and Samaria -> LOC places
    "23814": [("Stephanum", "PERSON")],
    "23815": [("Saulus", "PERSON")],
    "23817": [("Philippus", "PERSON"), ("Samariae", "LOC"), ("Christum", "PERSON")],
    # ciuitatem Samariae = city of Samaria -> LOC; Christum -> PERSON (Christ)
    "23818": [("Philippo", "PERSON")],
    "23822": [("Simon", "PERSON"), ("Samariae", "LOC")],
    # gentem Samariae = people of Samaria region; Samariae here LOC (region)
    "23827": [("Philippo", "PERSON"), ("Iesu Christi", "PERSON")],
    "23828": [("Simon", "PERSON")],
    "23829": [("Philippo", "PERSON")],
    "23831": [("Hierosolymis", "LOC"), ("Samaria", "LOC"), ("Petrum", "PERSON"),
              ("Iohannem", "PERSON")],
    # "recepit Samaria uerbum" Samaria the place/region -> LOC
    "23833": [("Iesu", "PERSON")],
    "23835": [("Simon", "PERSON")],
    "23837": [("Petrus", "PERSON")],
    "23845": [("Simon", "PERSON")],
    "23847": [("Hierosolymam", "LOC"), ("Samaritanorum", "NORP")],
    # regiones Samaritanorum = regions of the Samaritans -> NORP people
    "23848": [("Philippum", "PERSON")],
    "23849": [("Hierusalem", "LOC"), ("Gazam", "LOC")],
    "23852": [("Candacis", "PERSON"), ("Aethiopum", "NORP"), ("Hierusalem", "LOC")],
    # uir aethiops = an Ethiopian man (adj, leave); Candacis = Candace (queen) PERSON;
    # reginae Aethiopum = queen of the Ethiopians -> NORP
    "23853": [("Esaiam", "PERSON")],
    "23854": [("Philippo", "PERSON")],
    "23856": [("Philippus", "PERSON"), ("Esaiam", "PERSON")],
    "23860": [("Philippum", "PERSON")],
    "23867": [("Philippo", "PERSON")],
    "74908": [("Philippus", "PERSON"), ("Iesum", "PERSON")],
    "23877": [("Philippus", "PERSON")],
    "23878": [("Philippum", "PERSON")],
    "23880": [("Philippus", "PERSON"), ("Azoto", "LOC"), ("Caesaream", "LOC")],
    "26587": [("Iudaei", "NORP"), ("Graeci", "NORP")],
    "26588": [("Iudaeo", "NORP"), ("Graeco", "NORP")],
    "26595": [("Iudaeus", "NORP")],
}

# Drop the placeholder None-label entries (theological "Deus" not tagged).
for k in list(ANN):
    ANN[k] = [(s, lbl) for (s, lbl) in ANN[k] if lbl is not None]


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"]
    sl = data[474:632]

    out = []
    dropped = []
    for sent in sl:
        sid = str(sent["meta"]["sent_id"])
        text = sent["text"]
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
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}
    for rec in out:
        for e in rec["entities"]:
            counts[e["label"]] += 1

    print("WROTE:", OUT)
    print("SENTENCES:", len(out))
    print("COUNTS:", counts)
    print("TOTAL_ENTITIES:", sum(counts.values()))
    if dropped:
        print("DROPPED:")
        for sid, surf, lbl in dropped:
            print(f"  [{sid}] {surf!r} ({lbl}) - not a substring")
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
