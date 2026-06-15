#!/usr/bin/env python3
"""Build NER JSON for PROIEL test data[1106:1260].

Offsets computed deterministically via str.find (first occurrence default).
"multi": true when surface occurs >1 time. Non-substring surfaces dropped + logged.
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-proiel-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/proiel_1106_1260.json")

# Annotations keyed by sent_id. Each value: list of (surface, label).
# Surfaces copied EXACTLY from sentence text. Labels: PERSON / LOC / NORP.
ANN = {
    "52851": [("Diuiciacum", "PERSON"), ("Gallis", "NORP")],
    "52852": [("Ariouisti", "PERSON")],
    "52853": [("Caesaris", "PERSON"), ("Ariouistus", "PERSON")],
    "64226": [],
    "52854": [("Caesar", "PERSON"), ("Romani", "NORP")],
    "52855": [],
    "52856": [("Ariouistus", "PERSON"), ("Caesar", "PERSON")],
    "64227": [],
    "52857": [],
    "64228": [],
    "52858": [("Caesar", "PERSON"), ("Gallorum", "NORP"), ("Gallis", "NORP")],
    "52859": [("Caesarem", "PERSON")],
    "52860": [],
    "52973": [],
    "56939": [("Belgos", "NORP"), ("Germanis", "NORP"), ("Rhenum", "LOC"),
              ("Gallos", "NORP"), ("Gallia", "LOC"), ("Teutonos", "NORP"),
              ("Cimbros", "NORP")],
    "52974": [],
    "52975": [("Remi", "NORP"), ("Belgarum", "NORP")],
    "52976": [("Bellouacos", "NORP")],
    "63644": [],
    "52977": [("Suessiones", "NORP")],
    "52978": [],
    "52979": [("Diuiciacum", "PERSON"), ("Galliae", "LOC"), ("Britanniae", "LOC")],
    "52980": [("Galbam", "PERSON")],
    "52981": [],
    "52982": [("Neruios", "NORP")],
    "52983": [("Atrebates", "NORP"), ("Ambianos", "NORP"), ("Morinos", "NORP"),
              ("Menapios", "NORP"), ("Caletos", "NORP"), ("Ueliocasses", "NORP"),
              ("Uiromanduos", "NORP"), ("Atuatucos", "NORP")],
    "52984": [("Condrusos", "NORP"), ("Eburones", "NORP"), ("Caerosos", "NORP"),
              ("Paemanos", "NORP"), ("Germani", "NORP")],
    "52985": [("Caesar", "PERSON"), ("Remos", "NORP")],
    "52986": [],
    "52987": [("Diuiciacum", "PERSON"), ("Haeduum", "NORP")],
    "52988": [("Haedui", "NORP"), ("Bellouacorum", "NORP")],
    "52989": [],
    "52990": [("Belgarum", "NORP"), ("Remis", "NORP"), ("Axonam", "LOC"),
              ("Remorum", "NORP")],
    "52991": [("Remis", "NORP")],
    "52992": [],
    "52993": [("Quintum Titurium Sabinum", "PERSON")],
    "52994": [],
    "52995": [("Remorum", "NORP"), ("Bibrax", "LOC")],
    "52996": [("Belgae", "NORP")],
    "52997": [],
    "52998": [("Gallorum", "NORP"), ("Belgarum", "NORP")],
    "56940": [],
    "52999": [],
    "53000": [],
    "53001": [("Iccius", "PERSON"), ("Remus", "NORP"), ("Caesarem", "PERSON")],
    "56941": [],
    "53215": [("Caesar", "PERSON")],
    "53216": [],
    "53217": [("Bruto", "PERSON")],
    "53218": [],
    "53219": [("Gallis", "NORP")],
    "53220": [],
    "53221": [],
    "53222": [("Gallicis", "NORP")],
    "53223": [("Caesaris", "PERSON")],
    "53224": [],
    "53225": [],
    "53226": [],
    "53227": [],
    "53228": [],
    "63200": [],
    "53229": [("Uenetorum", "NORP")],
    "53230": [],
    "53231": [],
    "53232": [("Caesari", "PERSON")],
    "53233": [],
    "53234": [],
    "53235": [("Uenetis", "NORP"), ("Quintus Titurius Sabinus", "PERSON"),
              ("Caesare", "PERSON"), ("Uenellorum", "NORP")],
    "53236": [("Uiridouix", "PERSON")],
    "53237": [("Aulerci Eburouices", "NORP"), ("Lexouii", "NORP"),
              ("Uiridouice", "PERSON")],
    "53238": [("Gallia", "LOC")],
    "53239": [("Sabinus", "PERSON"), ("Uiridouix", "PERSON"), ("Sabinus", "PERSON")],
    "53240": [],
    "53241": [],
    "53242": [("Gallum", "NORP")],
    "53243": [],
    "53244": [("Romanorum", "NORP")],
    "63498": [("Caesar", "PERSON"), ("Uenetis", "NORP"), ("Sabinus", "PERSON"),
              ("Caesarem", "PERSON")],
    "53245": [],
    "53246": [("Gallos", "NORP"), ("Sabini", "PERSON"), ("Uenetici", "NORP")],
    "53247": [("Uiridouicem", "PERSON")],
    "53248": [("Romanorum", "NORP")],
    "53367": [("Germani", "NORP")],
    "53368": [],
    "53369": [],
    "53370": [],
    "53371": [("Rhenum", "LOC")],
    "63481": [("Caesar", "PERSON")],
    "53372": [("Germani", "NORP"), ("Mosae", "LOC"), ("Rheni", "LOC")],
    "53373": [],
    "53374": [("Caesar", "PERSON")],
    "53375": [("Gallorum", "NORP")],
    "53376": [("Caesar", "PERSON")],
    "53377": [("Caesar", "PERSON"), ("Rhenum", "LOC")],
    "53378": [("Germanos", "NORP"), ("Galliam", "LOC"), ("Romani", "NORP"),
              ("Rhenum", "LOC")],
    "53379": [("Usipetum", "NORP"), ("Tencterorum", "NORP"), ("Mosam", "LOC"),
              ("Rhenum", "LOC"), ("Sugambrorum", "NORP")],
    "53380": [("Caesar", "PERSON"), ("Galliae", "LOC"), ("Romani", "NORP"),
              ("Rhenum", "LOC")],
    "53381": [("Germanos", "NORP"), ("Galliam", "LOC"), ("Rhenum", "LOC")],
    "53382": [("Ubii", "NORP"), ("Transrhenanis", "NORP"), ("Caesarem", "PERSON"),
              ("Suebis", "NORP")],
    "53383": [("Rhenum", "LOC")],
    "63482": [],
    "53384": [("Ariouisto", "PERSON"), ("Germanorum", "NORP"), ("Romani", "NORP")],
    "53385": [],
    "54011": [("Mercurium", "PERSON")],
    "54012": [],
    "74721": [],
    "74722": [],
    "74723": [],
    "54013": [("Apollinem", "PERSON"), ("Martem", "PERSON"), ("Iouem", "PERSON"),
              ("Mineruam", "PERSON")],
    "54014": [],
    "74724": [("Apollinem", "PERSON"), ("Mineruam", "PERSON"), ("Iouem", "PERSON"),
              ("Martem", "PERSON")],
    "54015": [],
    "74725": [],
    "54016": [],
    "54017": [],
    "86051": [],
    "86052": [],
    "86053": [],
    "86054": [],
    "88124": [],
    "88125": [],
    "86055": [],
    "86056": [],
    "86057": [],
    "86058": [],
    "86059": [],
    "86060": [],
    "86061": [],
    "86062": [],
    "86064": [],
    "86065": [],
    "86066": [],
    "86067": [("Marce", "PERSON"), ("Plato", "PERSON")],
    "86068": [],
    "86069": [],
    "86070": [],
    "86071": [],
    "86073": [],
    "86074": [],
    "86075": [],
    "86076": [],
    "86077": [],
    "86078": [],
    "88126": [],
    "86079": [],
    "86080": [],
    "86081": [],
    "86082": [("Gaium Sulpicium", "PERSON"), ("Sextium Pompeium", "PERSON")],
    "86085": [],
    "86086": [],
    "86087": [],
    "86088": [],
    "86089": [],
    "86090": [],
}


def main():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"][1106:1260]

    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for sent in data:
        sid = sent["meta"]["sent_id"]
        text = sent["text"]
        pairs = ANN.get(sid, [])
        # Dedupe identical (surface,label) pairs: first occurrence + multi flag
        # already represents repeated surfaces; don't emit duplicate spans.
        seen = set()
        deduped = []
        for p in pairs:
            if p in seen:
                continue
            seen.add(p)
            deduped.append(p)
        pairs = deduped
        ents = []
        for surface, label in pairs:
            idx = text.find(surface)
            if idx == -1:
                dropped.append((sid, surface, label))
                continue
            multi = text.count(surface) > 1
            ent = {
                "text": surface,
                "label": label,
                "start": idx,
                "end": idx + len(surface),
                "multi": multi,
            }
            ents.append(ent)
            counts[label] += 1
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PATH:", OUT)
    print("SENTENCES:", len(out))
    print("COUNTS:", counts)
    print("DROPPED:", len(dropped))
    for sid, surf, lab in dropped:
        print(f"  DROP {sid} {lab} {surf!r}")


if __name__ == "__main__":
    main()
