"""The two documents a mailbox exports, and the one fold both are written with.

The fold and the escape used to be a private copy in each writer, and the copies disagreed - on
whether the first line may spend all 75 octets, and on whether a lone carriage return is a line
break. Now that there is one copy, its properties are asserted once here, over the whole length
range rather than at the three lengths a fixture happens to contain.

What each writer then does with it is a document, so it is compared byte for byte against a golden
rather than field by field: line order, escaping, folding and the ``X-MS-`` extensions are all in
the diff or in neither. Neither document is safe by construction: a parameter is not a TEXT field
and takes no backslashes, and a quoted-string may not contain a DQUOTE or a line break, so ``CN=``
needs its own encoding - which no golden can show unless the fixture carries the hostile input.
"""

from __future__ import annotations

import pytest
from office365.formats.text import MAX_LINE_OCTETS, escape_text, fold_line
from office365.migration.outlook.calendar_codec import attendee_line, encode, quote_param
from office365.migration.outlook.contacts_models import ContactRecord
from tests.unit.outlook_fixtures import document, sidecar

ATTENDEE = {
    "type": "required",
    "status": {"response": "accepted"},
    "emailAddress": {"name": "Bob", "address": "bob@contoso.com"},
}


def _attendee(name: str) -> str:
    line = attendee_line({**ATTENDEE, "emailAddress": {"name": name, "address": "bob@contoso.com"}})
    assert line is not None
    return line


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

    The two old copies differed exactly here - the first measured the line it had, the second a
    character it was about to add - so the property is stated over the range instead of at the
    boundary the two happened to agree on.
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
        # A lone carriage return is a line break too: the vCard copy only matched \r?\n and
        # wrote the bare CR into the document.
        ("a\rb", "a\\nb"),
    ],
)
def test_a_text_value_carries_the_four_escapes(value, expected):
    assert escape_text(value) == expected


@pytest.mark.parametrize("name", ["quarterly_review.ics", "contact.vcf", "contact_minimal.vcf"])
def test_no_golden_document_writes_a_line_over_the_limit(name):
    """Measured on the bytes of the golden, not on the writer that produced it."""
    for line in document(name).split(b"\r\n"):
        assert len(line) <= MAX_LINE_OCTETS, (name, len(line), line)


@pytest.mark.parametrize(
    ("name", "parameter"),
    [
        ("Bob", 'CN="Bob"'),
        # A quoted-string ends at the first DQUOTE, which is how the name took the line.
        ('Bob "Bobby"', "CN=\"Bob ^'Bobby^'\""),
        # A line break here used to end the ATTENDEE line and start a property of its own.
        ("Bob\r\nX-EVIL:1", 'CN="Bob^nX-EVIL:1"'),
        ("Bob\nX-EVIL:1", 'CN="Bob^nX-EVIL:1"'),
        # The separators are literal inside a quoted-string: no backslashes, no commas out.
        ("a;b,c:d", 'CN="a;b,c:d"'),
        ("Bob ^ Carter", 'CN="Bob ^^ Carter"'),
    ],
)
def test_a_parameter_value_cannot_end_its_line(name, parameter):
    line = _attendee(name)
    assert line.startswith(f"ATTENDEE;{parameter};ROLE=REQ-PARTICIPANT")
    assert "\r\n" not in line and "\n" not in line


def test_a_control_character_is_dropped_rather_than_rendered():
    """``^n`` carries a line break; a NUL and a tab have no place in a name."""
    assert quote_param("a\x00b\td") == '"abd"'


def test_a_line_break_in_an_organizer_name_does_not_become_a_property():
    envelope = {
        "subject": "x",
        "organizer": {"emailAddress": {"name": "Alice\r\nX-EVIL:1", "address": "alice@contoso.com"}},
    }
    lines = encode(envelope).decode("utf-8").split("\r\n")
    assert 'ORGANIZER;CN="Alice^nX-EVIL:1":mailto:alice@contoso.com' in lines
    assert not any(line.startswith("X-EVIL") for line in lines)


def test_a_folded_parameter_line_stays_within_the_limit():
    """A name long enough to fold is still a fold: the split lands inside the quotes."""
    rendered = encode(
        {"subject": "x", "attendees": [{**ATTENDEE, "emailAddress": {"name": "A" * 200, "address": "bob@contoso.com"}}]}
    )
    for line in rendered.split(b"\r\n"):
        assert len(line) <= MAX_LINE_OCTETS, (len(line), line)


def test_the_contact_writer_renders_the_golden_document():
    """One assertion for every branch: N/ADR slots, escaped text, folded lines, a list."""
    assert ContactRecord.from_json(sidecar("contact")).vcard() == document("contact.vcf")


def test_an_unset_value_leaves_no_line():
    """A contact with a name and an id renders six lines, not twenty empty ones."""
    rendered = document("contact_minimal.vcf")
    assert ContactRecord.from_json(sidecar("contact_minimal")).vcard() == rendered
    assert rendered.decode("utf-8").splitlines() == [
        "BEGIN:VCARD",
        "VERSION:3.0",
        "N:;;;;",
        "FN:Grace Hopper",
        "UID:c2",
        "END:VCARD",
    ]
