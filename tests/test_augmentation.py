"""Tests for casing augmentation of NER training items."""

import pytest

from scripts.build_training_data import augment_items


# ── helpers ──────────────────────────────────────────────────────────────────

def item(text: str, spans: list[dict] | None = None) -> dict:
    return {"text": text, "spans": spans or []}


# ── upper-variant tests ───────────────────────────────────────────────────────

def test_lowercase_start_produces_upper_variant():
    """Item starting with lowercase gets an uppercased-first-char variant."""
    result = augment_items([item("hic Caesar est.", [{"start": 4, "end": 10, "label": "PERSON"}])])
    texts = [i["text"] for i in result]
    assert "Hic Caesar est." in texts


def test_uppercase_start_skips_upper_variant():
    """Item already starting with uppercase does not get a duplicate upper variant."""
    result = augment_items([item("Hic Caesar est.", [{"start": 4, "end": 10, "label": "PERSON"}])])
    texts = [i["text"] for i in result]
    assert "Hic Caesar est." not in texts


# ── lower-variant tests ───────────────────────────────────────────────────────

def test_uppercase_start_non_entity_produces_lower_variant():
    """Item starting with uppercase non-entity token gets a lowercased-first-char variant."""
    result = augment_items([item("Hic Caesar est.", [{"start": 4, "end": 10, "label": "PERSON"}])])
    texts = [i["text"] for i in result]
    assert "hic Caesar est." in texts


def test_uppercase_start_entity_skips_lower_variant():
    """Item whose first token is an entity does not get a lowercased variant."""
    result = augment_items([item("Caesar uicit.", [{"start": 0, "end": 6, "label": "PERSON"}])])
    texts = [i["text"] for i in result]
    assert "caesar uicit." not in texts


def test_lowercase_start_skips_lower_variant():
    """Item already starting with lowercase does not get a duplicate lower variant."""
    result = augment_items([item("hic Caesar est.", [{"start": 4, "end": 10, "label": "PERSON"}])])
    texts = [i["text"] for i in result]
    assert "hic Caesar est." not in texts


# ── span integrity ────────────────────────────────────────────────────────────

def test_augmented_items_preserve_spans():
    """Augmented items carry the same span data as the original."""
    spans = [{"start": 4, "end": 10, "label": "PERSON"}]
    result = augment_items([item("hic Caesar est.", spans)])
    for aug in result:
        assert aug["spans"] == spans


# ── edge cases ────────────────────────────────────────────────────────────────

def test_empty_list_returns_empty():
    assert augment_items([]) == []


def test_no_spans_item_still_augments():
    """Item with no spans gets an upper variant (no entity to protect)."""
    result = augment_items([item("hic est.")])
    texts = [i["text"] for i in result]
    assert "Hic est." in texts


def test_originals_not_included_in_result():
    """augment_items returns only new items, never the originals."""
    originals = [
        item("hic Caesar est.", [{"start": 4, "end": 10, "label": "PERSON"}]),
        item("Hic Caesar est.", [{"start": 4, "end": 10, "label": "PERSON"}]),
    ]
    result = augment_items(originals)
    original_texts = {i["text"] for i in originals}
    for aug in result:
        assert aug["text"] not in original_texts
