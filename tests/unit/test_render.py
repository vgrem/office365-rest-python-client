"""What a terminal is shown: a table, one object, a link, and a sentence when there is nothing.

The renderer is asserted on its own, on payloads built by hand, because it must not import the
model: printing is never allowed to become a reason to send a request. Which fields are an
address is the type's answer (``TypeSchema.links``, the ``link`` facet) and is passed in, so the
last case here is the one that matters -- the caller's declaration wins over a spelling.
"""

from __future__ import annotations

import csv
import io
import json

from office365.runtime.render import (
    LINK_FIELDS,
    cell,
    hyperlink,
    origin_of,
    render,
    resolve,
)

#: A header row and one row per record, with nothing above or below it.
HEADER_AND_TWO_ROWS = 3

LISTS = [
    {"Title": "Documents", "ItemCount": 1200, "DefaultViewUrl": "/sites/x/Lists/Documents"},
    {"Title": "A title long enough that a terminal has to cut it somewhere sensible", "ItemCount": 3},
]


def test_a_table_has_a_header_row_and_no_class_name() -> None:
    drawn = render(LISTS, columns=["Title", "ItemCount"], headers=True)

    lines = drawn.splitlines()
    assert lines[0].split() == ["TITLE", "ITEMCOUNT"]
    # A header row over the rows, and nothing above it: no class name, no count banner.
    assert len(lines) == HEADER_AND_TWO_ROWS
    assert "ListCollection" not in drawn


def test_numbers_align_right_and_a_long_cell_is_elided_with_a_mark() -> None:
    drawn = render(LISTS, columns=["Title", "ItemCount"])
    rows = drawn.splitlines()[1:]

    # The number column is right-aligned, so both values end at the same place.
    assert rows[0].endswith("1200")
    assert rows[1].endswith("   3")
    assert len(rows[0]) == len(rows[1])
    # 48 wide means 47 characters and a mark: a cut name is never mistaken for a short one.
    assert rows[1][:48].endswith("\u2026")


def test_one_object_is_shown_as_fields_rather_than_a_one_row_table() -> None:
    drawn = render([{"Title": "Documents", "ItemCount": 1200}])

    assert drawn.splitlines() == ["Title      Documents", "ItemCount  1200"]


def test_nothing_found_is_a_sentence() -> None:
    assert render([], empty="No lists found.") == "No lists found."
    assert render([]) == ""


def test_a_machine_format_answers_an_empty_document_and_not_the_sentence() -> None:
    """`o365 … -o json | jq` receives `[]`; English belongs to the formats a person reads."""
    assert render([], "json", empty="No lists found.") == "[]"
    assert render([], "csv", empty="No lists found.") == ""


def test_a_server_relative_address_is_joined_to_the_origin() -> None:
    assert origin_of("https://contoso.sharepoint.com/sites/x/_api/") == "https://contoso.sharepoint.com"
    assert resolve(LISTS[0], "https://contoso.sharepoint.com") == (
        "https://contoso.sharepoint.com/sites/x/Lists/Documents"
    )


def test_the_types_declaration_says_which_column_is_an_address() -> None:
    payload = {"Path": "/sites/x/Path.aspx", "DefaultViewUrl": "/sites/x/Lists/Documents"}
    origin = "https://contoso.sharepoint.com"

    # `List` declares DefaultViewUrl; the vocabulary the type did not declare is not consulted.
    assert resolve(payload, origin, fields=("DefaultViewUrl",)) == origin + "/sites/x/Lists/Documents"
    assert resolve(payload, origin, fields=()) is None
    # And the columns are tried in declaration order, so an absolute address wins.
    assert resolve({"Url": "https://contoso.sharepoint.com/sites/x"}, origin, fields=("Url",)) == (
        "https://contoso.sharepoint.com/sites/x"
    )


def test_a_rest_address_is_a_link_only_when_a_browser_can_open_it() -> None:
    payload: dict = {}

    assert resolve(payload, resource_url="https://contoso.sharepoint.com/sites/x") == (
        "https://contoso.sharepoint.com/sites/x"
    )
    assert resolve(payload, resource_url="https://contoso.sharepoint.com/_api/Web/Lists(guid'1')") is None
    assert resolve(payload, resource_url="https://graph.microsoft.com/v1.0/users/1") is None


def test_a_link_is_drawn_only_when_it_was_asked_for() -> None:
    drawn = render(LISTS, columns=["Title"], origin="https://contoso.sharepoint.com", link="never")
    assert "\033]8;;" not in drawn

    url = "https://contoso.sharepoint.com/sites/x/Lists/Documents"
    linked = render(LISTS, columns=["Title"], origin="https://contoso.sharepoint.com", link="always")
    # The name carries the link; the padding does not, or a terminal that marks a hyperlink
    # would draw a dotted rule across the gap and it would read as a border between rows.
    assert hyperlink(url, "Documents") in linked
    assert hyperlink(url, "Documents".ljust(48)) not in linked
    assert linked.startswith("TITLE\n")


def test_the_other_formats_are_for_other_programs() -> None:
    assert json.loads(render(LISTS, "json"))[0]["Title"] == "Documents"
    assert render(LISTS, "url", origin="https://c.sharepoint.com").splitlines()[0] == (
        "https://c.sharepoint.com/sites/x/Lists/Documents"
    )
    assert list(csv.reader(io.StringIO(render(LISTS, "csv", columns=["Title", "ItemCount"]))))[1] == [
        "Documents",
        "1200",
    ]
    assert render(LISTS, "name", columns=["Title"]).splitlines()[0] == "Documents"
    assert render(LISTS, "tsv", columns=["ItemCount"]).splitlines()[1] == "1200"


def test_a_value_is_spelled_the_way_a_command_line_spells_it() -> None:
    from datetime import date, datetime

    assert cell(True) == ("true", False)
    assert cell(None) == ("", False)
    assert cell(1200) == ("1200", True)
    assert cell(datetime(2024, 5, 1, 9, 30, 15, 123456)) == ("2024-05-01 09:30:15", False)
    assert cell(date(2024, 5, 1)) == ("2024-05-01", False)
    assert cell({"a": 1}) == ('{"a": 1}', False)
    assert LINK_FIELDS[0] == "WebUrl"
