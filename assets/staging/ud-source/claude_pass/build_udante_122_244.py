#!/usr/bin/env python3
"""Build NER annotations for UDante test slice data[122:244].

Annotations decided by hand per ANNOTATION_RULES.md (PERSON/LOC/NORP).
This script computes char offsets deterministically via str.find,
marks multi=true when a surface occurs >1 time, and DROPS+logs any
surface that is not an exact substring of its sentence.
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-udante-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/udante_122_244.json")

# Hand annotations keyed by sent_id: list of (surface, label).
# Surfaces copied EXACTLY from the sentence text.
ANN = {
    # 122 DVE-91-c: demonyms (city/people groups) = NORP; placenames LOC
    "DVE-91-c": [
        ("Mediolanenses", "NORP"), ("Ueronenses", "NORP"),
        ("Romani", "NORP"), ("Florentini", "NORP"),
        ("Neapoletani", "NORP"), ("Caetani", "NORP"),
        ("Rauennates", "NORP"), ("Fauentini", "NORP"),
        ("Bononienses", "NORP"),  # occurs twice -> multi
        ("Burgi Sancti Felicis", "LOC"),
        ("Strate Maioris", "LOC"),
    ],
    "DVE-92": [],
    "DVE-93": [],
    "DVE-94": [("Deo", "PERSON")],  # God
    "DVE-95-a": [],
    "DVE-95-b": [],
    "DVE-96": [("Papienses", "NORP"), ("Papiensibus", "NORP")],
    "DVE-97-a": [],
    "DVE-97-b": [],
    "DVE-98": [],
    "DVE-99": [],
    "DVE-100-a": [],
    "DVE-100-b": [],
    "DVE-101": [],
    "DVE-102": [],
    # 137 DVE-103: Ytalis = Italians (NORP)
    "DVE-103": [("Ytalis", "NORP")],
    "DVE-104": [],
    # 139 DVE-105: Troianorum, Romanorum = NORP; Arturi = PERSON; Biblia = work (skip)
    "DVE-105": [
        ("Troianorum", "NORP"), ("Romanorum", "NORP"),
        ("Arturi", "PERSON"),
    ],
    # 140 DVE-106: Petrus de Aluernia = PERSON (named individual)
    "DVE-106": [("Petrus de Aluernia", "PERSON")],
    # 141 DVE-107-a: Latinorum = NORP; Cynus Pistoriensis = PERSON
    "DVE-107-a": [("Latinorum", "NORP"), ("Cynus Pistoriensis", "PERSON")],
    "DVE-107-b": [],
    # 143 DVE-108: latium = the Latin vernacular (region adj/metonym) -> LOC? "uulgare latium" = Latin vernacular. latium here adjectival. Skip (common adj for vernacular)
    "DVE-108": [],
    # 144 DVE-109: Latium = the Italian vernacular-region; Dante uses Latium = Italy region -> LOC
    "DVE-109": [("Latium", "LOC")],
    # 145 DVE-110-a: Apenini = mountain LOC; Lucanus = PERSON
    "DVE-110-a": [("Apenini", "LOC"), ("Lucanus", "PERSON")],
    # 146 DVE-110-b: Tyrenum mare (Tyrrhenian Sea) LOC; Adriaticum (Adriatic) LOC
    "DVE-110-b": [("Tyrenum mare", "LOC"), ("Adriaticum", "LOC")],
    # 147 DVE-111-a: Apulia, Roma, Ducatus, Tuscia, Ianuensis Marchia (regions)
    "DVE-111-a": [
        ("Apulia", "LOC"), ("Roma", "LOC"), ("Ducatus", "LOC"),
        ("Tuscia", "LOC"), ("Ianuensis Marchia", "LOC"),
    ],
    # 148 DVE-111-b: Apulie, Marchia Anconitana, Romandiola, Lombardia, Marchia Triuisiana, Uenetiis
    "DVE-111-b": [
        ("Apulie", "LOC"), ("Marchia Anconitana", "LOC"),
        ("Romandiola", "LOC"), ("Lombardia", "LOC"),
        ("Marchia Triuisiana", "LOC"), ("Uenetiis", "LOC"),
    ],
    # 149 DVE-112-a: Forum Iulii, Ystria = LOC; Ytalie = Italy LOC
    "DVE-112-a": [("Forum Iulii", "LOC"), ("Ystria", "LOC"), ("Ytalie", "LOC")],
    # 150 DVE-112-b: Tyreni maris, Sicilia, Sardinia, Ytalie (x2 -> multi), Ytaliam
    "DVE-112-b": [
        ("Tyreni maris", "LOC"), ("Sicilia", "LOC"), ("Sardinia", "LOC"),
        ("Ytalie", "LOC"), ("Ytaliam", "LOC"),
    ],
    # 151 DVE-113-a: all demonym groups NORP
    "DVE-113-a": [
        ("Siculorum", "NORP"), ("Apulis", "NORP"), ("Apulorum", "NORP"),
        ("Romanis", "NORP"), ("Romanorum", "NORP"), ("Spoletanis", "NORP"),
        ("Tuscis", "NORP"), ("Tuscorum", "NORP"), ("Ianuensibus", "NORP"),
        ("Ianuensium", "NORP"), ("Sardis", "NORP"),
    ],
    # 152 DVE-113-b: demonym groups NORP
    "DVE-113-b": [
        ("Calabrorum", "NORP"), ("Anconitanis", "NORP"),
        ("Romandiolis", "NORP"), ("Romandiolorum", "NORP"),
        ("Lombardis", "NORP"), ("Lombardorum", "NORP"),
        ("Triuisianis", "NORP"), ("Uenetis", "NORP"),
        ("Aquilegiensibus", "NORP"), ("Ystrianis", "NORP"),
    ],
    # 153 DVE-114: Latinorum = NORP
    "DVE-114": [("Latinorum", "NORP")],
    # 154 DVE-115: Ytalia = LOC
    "DVE-115": [("Ytalia", "LOC")],
    # 155 DVE-116-a: Tuscia LOC, Senenses/Aretini NORP, Lombardia LOC, Ferrarenses/Placentini NORP
    "DVE-116-a": [
        ("Tuscia", "LOC"), ("Senenses", "NORP"), ("Aretini", "NORP"),
        ("Lombardia", "LOC"), ("Ferrarenses", "NORP"), ("Placentini", "NORP"),
    ],
    "DVE-116-b": [],
    # 157 DVE-117: Ytalie LOC
    "DVE-117": [("Ytalie", "LOC")],
    # 158 DVE-118-a: Ytalie LOC
    "DVE-118-a": [("Ytalie", "LOC")],
    "DVE-118-b": [],
    # 160 DVE-119: Romani NORP
    "DVE-119": [("Romani", "NORP")],
    # 161 DVE-120-a: Romanorum NORP, ytalorum NORP
    "DVE-120-a": [("Romanorum", "NORP"), ("ytalorum", "NORP")],
    "DVE-120-b": [],
    "DVE-121": [],
    # 164 DVE-122: Anconitane Marchie LOC; Spoletanos NORP
    "DVE-122": [("Anconitane Marchie", "LOC"), ("Spoletanos", "NORP")],
    # 165 DVE-123-a: Florentinus NORP; Castra = PERSON (proper name of poet)
    "DVE-123-a": [("Florentinus", "NORP"), ("Castra", "PERSON")],
    "DVE-123-b": [],
    # 167 DVE-124: Mediolanenses, Pergameos NORP
    "DVE-124": [("Mediolanenses", "NORP"), ("Pergameos", "NORP")],
    # 168 DVE-125: Aquilegienses, Ystrianos NORP
    "DVE-125": [("Aquilegienses", "NORP"), ("Ystrianos", "NORP")],
    # 169 DVE-126: Casentinenses, Fractenses NORP
    "DVE-126": [("Casentinenses", "NORP"), ("Fractenses", "NORP")],
    # 170 DVE-127-a: Sardos NORP; Latii (=of Latium/Italy, here people? "non Latii sunt" = are not of Latium) -> NORP demonym; Latiis NORP
    "DVE-127-a": [("Sardos", "NORP"), ("Latii", "NORP"), ("Latiis", "NORP")],
    "DVE-127-b": [],
    # 172 DVE-128: ytalis (uulgaribus ytalis = Italian vernaculars) NORP demonym adj
    "DVE-128": [("ytalis", "NORP")],
    "DVE-129-a": [],
    # 174 DVE-129-b: Ytali NORP
    "DVE-129-b": [("Ytali", "NORP")],
    # 175 DVE-130: trinacrie terre = Sicily (Trinacria) LOC; ytalorum NORP
    "DVE-130": [("trinacrie terre", "LOC"), ("ytalorum", "NORP")],
    # 176 DVE-131: Fredericus Cesar PERSON; Manfredus PERSON
    "DVE-131": [("Fredericus Cesar", "PERSON"), ("Manfredus", "PERSON")],
    # 177 DVE-132-a: Latinorum NORP
    "DVE-132-a": [("Latinorum", "NORP")],
    # 178 DVE-132-b: Sicilia LOC
    "DVE-132-b": [("Sicilia", "LOC")],
    "DVE-133": [],
    # 180 DVE-134: Frederici PERSON; Karoli PERSON; Iohannis PERSON; Azonis PERSON
    "DVE-134": [
        ("Frederici", "PERSON"), ("Karoli", "PERSON"),
        ("Iohannis", "PERSON"), ("Azonis", "PERSON"),
    ],
    "DVE-135": [],
    # 182 DVE-136: Siculorum NORP
    "DVE-136": [("Siculorum", "NORP")],
    # 183 DVE-137-a: Apuli NORP; Romani NORP; Marchiani NORP
    "DVE-137-a": [("Apuli", "NORP"), ("Romani", "NORP"), ("Marchiani", "NORP")],
    # 184 DVE-137-b: Apuli NORP
    "DVE-137-b": [("Apuli", "NORP")],
    # 185 DVE-138: Ytalia LOC
    "DVE-138": [("Ytalia", "LOC")],
    # 186 DVE-139: Tuscos NORP
    "DVE-139": [("Tuscos", "NORP")],
    # 187 DVE-140: named poets PERSON (maximal proper-name spans, drop appellatives but keep epithet surnames as part of name)
    "DVE-140": [
        ("Guittonem Aretinum", "PERSON"),
        ("Bonagiuntam Lucensem", "PERSON"),
        ("Gallum Pisanum", "PERSON"),
        ("Minum Mocatum Senensem", "PERSON"),
        ("Brunectum Florentinum", "PERSON"),
    ],
    # 188 DVE-141: Tusci NORP; Tuscanorum NORP
    "DVE-141": [("Tusci", "NORP"), ("Tuscanorum", "NORP")],
    # 189 DVE-142: Florentini NORP
    "DVE-142": [("Florentini", "NORP")],
    # 190 DVE-143: Pisani NORP; Fiorensa LOC (vernacular Florence); Pisa LOC
    "DVE-143": [("Pisani", "NORP"), ("Fiorensa", "LOC"), ("Pisa", "LOC")],
    # 191 DVE-144: Lucenses NORP; Dio PERSON (God); Lucca LOC
    "DVE-144": [("Lucenses", "NORP"), ("Dio", "PERSON"), ("Lucca", "LOC")],
    # 192 DVE-145-1: Senenses NORP; Siena LOC
    "DVE-145-1": [("Senenses", "NORP"), ("Siena", "LOC")],
    # 193 DVE-145-2: Aretini NORP
    "DVE-145-2": [("Aretini", "NORP")],
    # 194 DVE-145-3: Perusio, Urbe Ueteri, Uiterbio, Ciuitate Castellana LOC; Romanis, Spoletanis NORP
    "DVE-145-3": [
        ("Perusio", "LOC"), ("Urbe Ueteri", "LOC"), ("Uiterbio", "LOC"),
        ("Ciuitate Castellana", "LOC"),
        ("Romanis", "NORP"), ("Spoletanis", "NORP"),
    ],
    # 195 DVE-146: Tusci NORP; named poets PERSON; Florentinos NORP; Cynum Pistoriensem PERSON
    "DVE-146": [
        ("Tusci", "NORP"), ("Guidonem", "PERSON"), ("Lapum", "PERSON"),
        ("Florentinos", "NORP"), ("Cynum Pistoriensem", "PERSON"),
    ],
    # 196 DVE-147: Tuscanorum NORP
    "DVE-147": [("Tuscanorum", "NORP")],
    # 197 DVE-148: Tuscis NORP; Ianuensibus NORP; Ianuenses NORP
    "DVE-148": [("Tuscis", "NORP"), ("Ianuensibus", "NORP"), ("Ianuenses", "NORP")],
    "DVE-149": [],
    # 199 DVE-150: Apenini LOC; Ytaliam LOC
    "DVE-150": [("Apenini", "LOC"), ("Ytaliam", "LOC")],
    # 200 DVE-151: Romandiolam LOC; Latio LOC
    "DVE-151": [("Romandiolam", "LOC"), ("Latio", "LOC")],
    "DVE-152": [],
    # 202 DVE-153-a: Romandiolos NORP; Forliuienses NORP
    "DVE-153-a": [("Romandiolos", "NORP"), ("Forliuienses", "NORP")],
    "DVE-153-b": [],
    # 204 DVE-154: Thomam PERSON; Ugolinum Bucciolam PERSON; Fauentinos NORP
    "DVE-154": [("Thomam", "PERSON"), ("Ugolinum Bucciolam", "PERSON"), ("Fauentinos", "NORP")],
    "DVE-155": [],
    # 206 DVE-156-a: Brixianos, Ueronenses, Uigentinos NORP
    "DVE-156-a": [("Brixianos", "NORP"), ("Ueronenses", "NORP"), ("Uigentinos", "NORP")],
    # 207 DVE-156-b: Paduanos NORP
    "DVE-156-b": [("Paduanos", "NORP")],
    # 208 DVE-157: Triuisianos NORP; Brixianorum NORP
    "DVE-157": [("Triuisianos", "NORP"), ("Brixianorum", "NORP")],
    # 209 DVE-158: Ueneti NORP; Dio PERSON; Ildebrandinum Paduanum PERSON
    "DVE-158": [("Ueneti", "NORP"), ("Dio", "PERSON"), ("Ildebrandinum Paduanum", "PERSON")],
    "DVE-159": [],
    # 211 DVE-160: ytalia (silua) = Italy LOC adj
    "DVE-160": [("ytalia", "LOC")],
    # 212 DVE-161: Bononienses NORP; Ymolensibus, Ferrarensibus, Mutinensibus NORP; Sordellus de Mantua PERSON; Mantua LOC; Cremone, Brixie, Uerone LOC
    "DVE-161": [
        ("Bononienses", "NORP"), ("Ymolensibus", "NORP"),
        ("Ferrarensibus", "NORP"), ("Mutinensibus", "NORP"),
        ("Sordellus de Mantua", "PERSON"),
        ("Cremone", "LOC"), ("Brixie", "LOC"), ("Uerone", "LOC"),
    ],
    # 213 DVE-162-a: Ymolensibus, Ferrarensibus, Mutinensibus NORP; Lombardorum NORP
    "DVE-162-a": [
        ("Ymolensibus", "NORP"), ("Ferrarensibus", "NORP"),
        ("Mutinensibus", "NORP"), ("Lombardorum", "NORP"),
    ],
    # 214 DVE-162-b: Longobardorum NORP
    "DVE-162-b": [("Longobardorum", "NORP")],
    # 215 DVE-163-a: Ferrarensium, Mutinensium, Regianorum NORP
    "DVE-163-a": [("Ferrarensium", "NORP"), ("Mutinensium", "NORP"), ("Regianorum", "NORP")],
    "DVE-163-b": [],
    # 217 DVE-164: Parmensibus NORP
    "DVE-164": [("Parmensibus", "NORP")],
    # 218 DVE-165: Bononienses NORP
    "DVE-165": [("Bononienses", "NORP")],
    # 219 DVE-166-a: Latinorum NORP
    "DVE-166-a": [("Latinorum", "NORP")],
    # 220 DVE-166-b: bononiense (uulgare) = Bolognese NORP adj
    "DVE-166-b": [("bononiense", "NORP")],
    # 221 DVE-167: Guido Guinizelli, Guido Ghisilerius, Fabrutius, Honestus PERSON; Bononie LOC
    "DVE-167": [
        ("Guido Guinizelli", "PERSON"), ("Guido Ghisilerius", "PERSON"),
        ("Fabrutius", "PERSON"), ("Honestus", "PERSON"), ("Bononie", "LOC"),
    ],
    # 222 DVE-168-a: Guido PERSON
    "DVE-168-a": [("Guido", "PERSON")],
    # 223 DVE-168-b: Guido Ghisilerius PERSON
    "DVE-168-b": [("Guido Ghisilerius", "PERSON")],
    # 224 DVE-168-c: Fabrutius PERSON
    "DVE-168-c": [("Fabrutius", "PERSON")],
    # 225 DVE-168-d: Honestus PERSON
    "DVE-168-d": [("Honestus", "PERSON")],
    # 226 DVE-169: Bononie LOC
    "DVE-169": [("Bononie", "LOC")],
    # 227 DVE-170: Ytalie LOC
    "DVE-170": [("Ytalie", "LOC")],
    # 228 DVE-171-a: Tridentum, Taurinum, Alexandriam LOC; Ytalie LOC
    "DVE-171-a": [
        ("Tridentum", "LOC"), ("Taurinum", "LOC"),
        ("Alexandriam", "LOC"), ("Ytalie", "LOC"),
    ],
    # 229 DVE-171-b: latium (uere latium = truly Latin/Italian) adj -> skip (predicate adj)
    "DVE-171-b": [],
    # 230 DVE-172: latium adj (illustre) -> skip
    "DVE-172": [],
    # 231 DVE-173: Ytalie LOC
    "DVE-173": [("Ytalie", "LOC")],
    "DVE-174": [],
    "DVE-175": [],
    "DVE-176": [],
    "DVE-177-a": [],
    "DVE-177-b": [],
    "DVE-177-c": [],
    # 238 DVE-177-d: latini (homines latini) NORP; Latinorum NORP
    "DVE-177-d": [("latini", "NORP"), ("Latinorum", "NORP")],
    # 239 DVE-178-a: Ytalie LOC
    "DVE-178-a": [("Ytalie", "LOC")],
    "DVE-178-b": [],
    # 241 DVE-179-a: Deus PERSON (God)
    "DVE-179-a": [("Deus", "PERSON")],
    "DVE-179-b": [],
    "DVE-179-c": [],
}


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))["data"][122:244]
    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for sent in data:
        sid = sent["meta"]["sent_id"]
        text = sent["text"]
        pairs = ANN.get(sid, [])
        ents = []
        for surface, label in pairs:
            start = text.find(surface)
            if start == -1:
                dropped.append((sid, surface, label))
                continue
            end = start + len(surface)
            multi = text.count(surface) > 1
            ents.append({
                "text": surface,
                "label": label,
                "start": start,
                "end": end,
                "multi": multi,
            })
            counts[label] += 1
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    print(f"TOTAL ENTITIES: {sum(counts.values())}")
    if dropped:
        print(f"DROPPED ({len(dropped)}):")
        for sid, surf, lab in dropped:
            print(f"  - [{sid}] {lab} {surf!r} (not a substring)")
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
