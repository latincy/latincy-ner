# LatinCy NER annotation rules (bootstrap pass) — v0 draft

Three labels only. Copy entity surfaces EXACTLY (char-for-char, same capitalization) from the
sentence text.

## PERSON
Named individuals; Greco-Roman deities (Iuppiter, Venus, Apollo, Bacchus, Mercurius); named
mythological/heroic figures (Aeneas, Turnus, Dido, Ulixes); biblical persons (Iesus, Petrus,
Paulus, Moyses, David, Abraham); CLOSED mythological groups whose membership is fixed
(Gigantes, Parcae, Musae).

## LOC
Any place — cities, countries, regions, rivers, mountains, seas, lakes (Troia, Roma, Italia,
Gallia, Aegyptus, Iudaea, Hierusalem, Tiberis, Olympus, Latium, Carthago). LOC merges GPE +
physical location (no separate GPE label).

## NORP  ← most under-tagged; actively hunt these
Nationality / ethnic / religious / political groups, INCLUDING demonym adjectives and
substantivized demonyms, in ALL case forms:
- ethnonyms: Romani, Galli, Helvetii, Belgae, Germani, Troes/Troiani, Danai, Argivi, Achivi,
  Graii/Graeci, Poeni, Latini, Itali, Rutuli, Tyrii, Phryges, Pelasgi (Romanorum, Gallorum,
  Teucris, Danaum, ...).
- religious/political groups: Iudaei, Pharisaei, Sadducaei, Samaritani, Christiani, Gentiles.

## Key distinctions
- PERSON vs NORP: closed, fixed-membership set → PERSON (Gigantes); open group identity → NORP
  (Romani, Iudaei). Test: "can new members be born into / join the group?" yes → NORP.
- Place form vs people form: Troia / Roma / Iudaea = LOC; Troes / Romani / Iudaei = NORP. Tag
  what actually appears in the text.
- Metonymy: tag by what the word denotes in context (function over form).

## Boundaries
- Tag the maximal proper-name span; multi-token names are ONE span (Gaius Iulius Caesar).
- EXCLUDE attached common-noun titles/appellatives: "pater Aeneas" → tag "Aeneas"; "rex
  Latinus" → tag "Latinus"; "Pontifex Maximus" → not tagged.

## Do NOT tag
Generic common nouns; works/books (Aeneis); events/festivals; dates; institutions (Senatus,
ecclesia); animal names; substantivized product adjectives (Falernum = wine, Corintheum = ware).

## Output format (write via Python; compute offsets deterministically)
Per sentence: decide (surface, label) pairs copied exactly from text. Then a Python script:
find each surface via str.find (default first occurrence; add "multi": true if it occurs more
than once; DROP and log any surface that is not an exact substring). Emit a JSON list of
{"sent_id", "text", "entities":[{"text","label","start","end","multi"}]}.
