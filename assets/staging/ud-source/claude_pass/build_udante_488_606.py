"""Deterministic offset computation for UDante test data[488:606].

Manually-decided (surface, label) pairs per sentence (copied EXACTLY from text).
Offsets via str.find (first occurrence). multi:true if surface occurs >1 time.
Non-substring surfaces are DROPPED and logged.
"""
import json
from pathlib import Path

SRC = Path("assets/staging/ud-source/ud-udante-test.json")
OUT = Path("assets/staging/ud-source/claude_pass/udante_488_606.json")

# sent_id -> list of (surface, label[, occurrence_index])
# occurrence_index (0-based) selects which occurrence to anchor when a surface
# appears more than once and distinct occurrences must be tagged separately.
ANN = {
    "DVE-357-b": [("Arnaldus Danielis", "PERSON")],
    "DVE-383-a": [("Guidonis", "PERSON"), ("Florentia", "LOC")],
    "DVE-384-a": [("Yspani", "NORP"), ("Yspanos", "NORP")],
    "DVE-384-b": [("Namericus", "PERSON"), ("Belnui", "LOC")],
    "DVE-388-a": [
        ("Guidonem Guinizelli", "PERSON"),
        ("Guidonem", "PERSON", 1),  # second "Guidonem" (Guidonem de Ghisileriis)
        ("Ghisileriis", "LOC"),
        ("Fabrutium", "PERSON"),
        ("Bononienses", "NORP"),
    ],
    "DVE-391-b": [("Guidonis", "PERSON"), ("Florentini", "NORP")],
    "DVE-399-b": [("Arnaldus Danielis", "PERSON")],
    "DVE-403-a": [("Gottus Mantuanus", "PERSON")],
}


def nth_find(text: str, surface: str, n: int) -> int:
    """Return offset of the (0-based) n-th occurrence, or -1."""
    idx = -1
    for _ in range(n + 1):
        idx = text.find(surface, idx + 1)
        if idx == -1:
            return -1
    return idx


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    data = d["data"]
    out = []
    dropped = []
    counts = {"PERSON": 0, "LOC": 0, "NORP": 0}

    for i in range(488, len(data)):
        rec = data[i]
        text = rec["text"]
        sid = rec["meta"]["sent_id"]
        ents = []
        for spec in ANN.get(sid, []):
            surface, label = spec[0], spec[1]
            occ = spec[2] if len(spec) > 2 else 0
            start = nth_find(text, surface, occ)
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
            counts[label] += 1
        out.append({"sent_id": sid, "text": text, "entities": ents})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE: {OUT}")
    print(f"SENTENCES: {len(out)}")
    print(f"COUNTS: {counts}")
    print(f"TOTAL ENTITIES: {sum(counts.values())}")
    if dropped:
        for sid, surf, lab in dropped:
            print(f"DROPPED: {sid} {lab} {surf!r} (not a substring)")
    else:
        print("DROPPED: none")


if __name__ == "__main__":
    main()
