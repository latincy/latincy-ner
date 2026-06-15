"""Tests for the singles validator (scripts/validate_single.py).

Covers the Phase-3 invariant (declared authorities must cover used kb_id
namespaces) and the structural checks, on synthetic singles written to a tmp
file — so the suite is independent of the real assets/.
"""

import json

import pytest

from scripts.validate_single import kb_id_prefix, validate_single


def _write(tmp_path, single):
    p = tmp_path / "single.json"
    p.write_text(json.dumps(single), encoding="utf-8")
    return p


def _single(spans, authorities=None, tagset=("PERSON", "LOC")):
    annotation = {"tagset": list(tagset)}
    if authorities is not None:
        annotation["nel"] = {"authorities": authorities}
    return {
        "metadata": {"title": "t"},
        "annotation": annotation,
        "data": [{"text": "Perseus uicit.", "spans": spans}],
    }


@pytest.mark.parametrize(
    "kb_id,expected",
    [
        ("Q130832", "wd"),
        ("lkb:misc:harvey:agre", "lkb"),
        ("NIL0042", "NIL"),
        ("NIL", "NIL"),
    ],
)
def test_kb_id_prefix(kb_id, expected):
    assert kb_id_prefix(kb_id) == expected


def test_valid_wikidata_single_passes(tmp_path):
    single = _single(
        [{"start": 0, "end": 7, "label": "PERSON", "surface": "Perseus", "kb_id": "Q130832"}],
        authorities=[{"prefix": "wd", "name": "Wikidata"}],
    )
    assert validate_single(_write(tmp_path, single)) == []


def test_undeclared_authority_fails(tmp_path):
    # uses lkb but declares only wd → invariant violation
    single = _single(
        [{"start": 0, "end": 7, "label": "PERSON", "surface": "Perseus",
          "kb_id": "lkb:person:harvey:perseus"}],
        authorities=[{"prefix": "wd", "name": "Wikidata"}],
    )
    errs = validate_single(_write(tmp_path, single))
    assert any("lkb" in e and "not declared" in e for e in errs)


def test_nil_needs_no_authority(tmp_path):
    single = _single(
        [{"start": 0, "end": 7, "label": "PERSON", "surface": "Perseus", "kb_id": "NIL0042"}],
        authorities=[{"prefix": "wd", "name": "Wikidata"}],
    )
    assert validate_single(_write(tmp_path, single)) == []


def test_surface_mismatch_fails(tmp_path):
    single = _single(
        [{"start": 0, "end": 7, "label": "PERSON", "surface": "WRONG", "kb_id": "Q130832"}],
        authorities=[{"prefix": "wd", "name": "Wikidata"}],
    )
    errs = validate_single(_write(tmp_path, single))
    assert any("surface" in e for e in errs)


def test_offset_out_of_range_fails(tmp_path):
    single = _single(
        [{"start": 0, "end": 999, "label": "PERSON"}],
    )
    errs = validate_single(_write(tmp_path, single))
    assert any("out of range" in e for e in errs)


def test_label_not_in_tagset_fails(tmp_path):
    single = _single(
        [{"start": 0, "end": 7, "label": "MISC"}],
        tagset=("PERSON", "LOC"),
    )
    errs = validate_single(_write(tmp_path, single))
    assert any("not in tagset" in e for e in errs)


def test_missing_top_level_key_fails(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"metadata": {}, "data": []}), encoding="utf-8")
    errs = validate_single(p)
    assert any("annotation" in e for e in errs)


def test_ner_only_single_passes(tmp_path):
    # no nel block, no kb_id → nothing to resolve
    single = _single([{"start": 0, "end": 7, "label": "PERSON"}])
    assert validate_single(_write(tmp_path, single)) == []
