"""The line mechanics both documents share: one fold, one escape, one parameter rule.

Both writers used to carry a private copy, and the copies disagreed — on whether the first
line may spend all 75 octets, and on whether a lone carriage return is a line break. Now
that there is one copy, the properties are asserted once, here, over the whole length
range rather than at the three lengths a fixture happens to contain; the goldens in
``fixtures/outlook/`` then only have to say what the composed documents look like.
"""

from __future__ import annotations

import pytest
from office365.formats.text import MAX_LINE_OCTETS, escape_text, fold_line
from tests.unit.outlook_fixtures import document


def _widths(line: str) -> list[int]:
    return [len(part.encode("utf-8")) for part in line.split("\r\n")]


@pytest.mark.parametrize(("octets", "folds"), [(2, False), (75, False), (76, True), (150, True), (151, True)])
def test_the_first_line_spends_the_whole_allowance(octets, folds):
    """A line is folded when it is *over* 75 octets, not when it reaches it."""
    folded = fold_line("X:" + "a" * (octets - 2))
    assert ("\r\n" in folded) is folds
    assert _widths(folded)[0] == min(octets, MAX_LINE_OCTETS)


def test_a_continuation_pays_for_its_leading_space():
    """75 octets is the cap for every physical line, the continuation space included."""
    folded = fold_line("X:" + "a" * 200)
    assert folded.split("\r\n")[1].startswith(" ")
    assert max(_widths(folded)) == MAX_LINE_OCTETS


def test_the_fold_neither_loses_nor_splits_a_character():
    """From 0 to 200 octets, one byte at a time: what goes in comes back out.

    The old vCard fold and the old iCalendar fold differed exactly here — the first
    measured the line it had, the second a character it was about to add — so the property
    is stated over the range instead of at the boundary the two agreed on.
    """
    for octets in range(201):
        line = "SUMMARY:" + "a" * octets
        folded = fold_line(line)
        assert folded.replace("\r\n ", "") == line, octets
        assert max(_widths(folded)) <= MAX_LINE_OCTETS, octets


def test_a_multi_byte_character_stays_whole_under_the_octet_count():
    """The budget is octets, the fold is at character boundaries: ``é`` is two of them."""
    line = "SUMMARY:" + "é" * 100
    folded = fold_line(line)
    assert folded.replace("\r\n ", "") == line
    assert max(_widths(folded)) <= MAX_LINE_OCTETS


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, ""),
        ("plain", "plain"),
        ("a;b,c", "a\\;b\\,c"),
        ("a\\b", "a\\\\b"),
        ("a\nb", "a\\nb"),
        ("a\r\nb", "a\\nb"),
        # A lone carriage return is a line break too: the vCard copy only matched \r?\n
        # and wrote the bare CR into the document.
        ("a\rb", "a\\nb"),
    ],
)
def test_a_text_value_carries_the_four_escapes(value, expected):
    assert escape_text(value) == expected


@pytest.mark.parametrize("name", ["quarterly_review.ics", "contact.vcf", "contact_minimal.vcf"])
def test_no_document_writes_a_line_over_the_limit(name):
    """Measured on the bytes of the golden, not on the writer that produced it."""
    for line in document(name).split(b"\r\n"):
        assert len(line) <= MAX_LINE_OCTETS, (name, len(line), line)
