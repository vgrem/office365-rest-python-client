"""The ``.ics`` line mechanics: a value cannot end the line it sits on, and a fold can.

The golden document in ``fixtures/outlook/`` pins what a fully populated event renders to.
This file pins the two ways a *value* escapes its slot, neither of which a golden can
show unless the fixture happens to carry the hostile input: a parameter is not a TEXT
field and takes no backslashes, and a quoted-string may not contain a DQUOTE or a line
break — so ``CN=`` needs its own encoding, and the fold has to hold afterwards.
"""

from __future__ import annotations

import pytest
from office365.migration.outlook.calendar_codec import (
    MAX_LINE_OCTETS,
    attendee_line,
    encode,
    quote_param,
)

ATTENDEE = {
    "type": "required",
    "status": {"response": "accepted"},
    "emailAddress": {"name": "Bob", "address": "bob@contoso.com"},
}


def _attendee(name: str) -> str:
    line = attendee_line({**ATTENDEE, "emailAddress": {"name": name, "address": "bob@contoso.com"}})
    assert line is not None
    return line


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
    document = encode(
        {"subject": "x", "attendees": [{**ATTENDEE, "emailAddress": {"name": "A" * 200, "address": "bob@contoso.com"}}]}
    )
    for line in document.split(b"\r\n"):
        assert len(line) <= MAX_LINE_OCTETS, (len(line), line)
