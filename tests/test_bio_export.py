"""Tests for BIO TSV export helper."""

import spacy
import pytest

from scripts.build_training_data import make_bio_lines, make_doc


@pytest.fixture(scope="module")
def nlp():
    return spacy.blank("la")


def test_single_token_entity_gets_b_tag(nlp):
    """Single-token entity is tagged B-LABEL."""
    item = {"text": "Caesar uicit.", "spans": [{"start": 0, "end": 6, "label": "PERSON"}]}
    doc = make_doc(nlp, item)
    pairs = dict(make_bio_lines(doc))
    assert pairs["Caesar"] == "B-PERSON"


def test_non_entity_token_gets_o_tag(nlp):
    """Non-entity tokens are tagged O."""
    item = {"text": "Caesar uicit.", "spans": [{"start": 0, "end": 6, "label": "PERSON"}]}
    doc = make_doc(nlp, item)
    pairs = dict(make_bio_lines(doc))
    assert pairs["uicit"] == "O"


def test_multi_token_entity_b_then_i(nlp):
    """Multi-token entity: first token B-LABEL, continuation token I-LABEL."""
    item = {"text": "Iulius Caesar uicit.", "spans": [{"start": 0, "end": 13, "label": "PERSON"}]}
    doc = make_doc(nlp, item)
    lines = make_bio_lines(doc)
    tags = {text: tag for text, tag in lines}
    assert tags["Iulius"] == "B-PERSON"
    assert tags["Caesar"] == "I-PERSON"
    assert tags["uicit"] == "O"


def test_no_entities_all_o(nlp):
    """Sentence with no entity spans produces all O tags."""
    item = {"text": "hic est.", "spans": []}
    doc = make_doc(nlp, item)
    lines = make_bio_lines(doc)
    assert lines  # non-empty
    assert all(tag == "O" for _, tag in lines)


def test_empty_doc_returns_empty_list(nlp):
    """Empty text produces no BIO lines."""
    item = {"text": "", "spans": []}
    doc = make_doc(nlp, item)
    assert make_bio_lines(doc) == []


def test_returns_list_of_tuples(nlp):
    """make_bio_lines returns a list of (str, str) pairs."""
    item = {"text": "Roma erat.", "spans": [{"start": 0, "end": 4, "label": "LOC"}]}
    doc = make_doc(nlp, item)
    lines = make_bio_lines(doc)
    assert isinstance(lines, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in lines)
