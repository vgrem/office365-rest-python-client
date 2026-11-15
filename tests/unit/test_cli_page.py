"""A node's page, and the two ways to ask for it.

``kubectl``, ``gh`` and ``docker`` all answer a bare group with the verbs it holds, grouped by
what they do, and answer ``<group> <cmd> -h`` with that command's arguments. ``o365 sharepoint
web`` used to answer one comma-joined line; the page here reads the same facts off the model:

* the actions are the stamped verbs (``office365.runtime.verbs``), so a word the router refused
  can never be printed;
* the groups are the effect each declares, so a destructive action is not listed as a read;
* the links are the getters the walk accepts;
* the sentence for a role is one line in the command line, because a role is a closed
  vocabulary and its text would otherwise be repeated on 4,000 methods;
* an ``action``'s sentence is the service's own summary, which the generator wrote from the
  metadata, and is printed only when the docstring opens with one.

The tests read a real product because the point is the agreement between the page and the model;
they do not send a request, and neither does the page.
"""

from __future__ import annotations

import argparse

import pytest
from office365.cli import _page, _sentence, main
from office365.routing import route
from office365.runtime.odata.query_options import QueryOptions

#: A page wraps its links and stops; six lines is the twelve words plus the "and N more" line.
PAGE_LINK_LINES = 6
#: What ``main`` returns for a word it refuses.
REFUSED = 2
#: A header row and the two rows of a two-item feed.
HEADER_AND_TWO_ROWS = 3


@pytest.fixture(scope="module")
def web() -> str:
    found = route("sharepoint", "web")
    return _page("sharepoint", "web", found)


def test_a_node_page_groups_its_actions_by_what_they_do(web: str) -> None:
    assert web.splitlines()[0] == "sharepoint web — Web"
    for heading in ("READ", "WRITE", "DESTROY"):
        assert f"\n{heading}\n" in web
    # `get` and `list` are declared read, `delete` is declared destroy: the heading says which.
    read = web.split("\nREAD\n")[1].split("\nWRITE\n", maxsplit=1)[0]
    destroy = web.split("\nDESTROY\n")[1]
    assert "  get  " in read and "  list  " in read
    assert "  delete  " in destroy and "  get  " not in destroy


def test_the_role_sentence_is_the_command_lines_own_words(web: str) -> None:
    assert "  get     read this one back" in web
    assert "  delete  remove this one" in web


def test_the_columns_a_read_shows_are_the_types_ranked_defaults(web: str) -> None:
    from office365.runtime.schema import TypeSchema
    from office365.sharepoint.webs.web import Web

    assert "a read shows " + ", ".join(TypeSchema.of(Web).defaults) in web
    assert "list --columns " + ",".join(TypeSchema.of(Web).defaults) in web


def test_the_page_lists_links_but_stops_being_a_wall(web: str) -> None:
    links = web.split("\nLINK\n")[1].split("\nTRY\n", maxsplit=1)[0]

    assert "lists" in links.split() and "webs" in links.split()
    # `Web` holds dozens of getters; a page shows twelve and says how many it left to a TAB.
    assert "more; a TAB offers every one" in links
    assert len(links.splitlines()) <= PAGE_LINK_LINES


def test_the_examples_are_lines_that_work(web: str) -> None:
    try_lines = [line.strip() for line in web.split("\nTRY\n")[1].splitlines() if line.strip().startswith("o365")]

    assert try_lines[0] == "o365 sharepoint web get"
    # The link example names a feed, so it reads something back instead of walking nowhere.
    assert try_lines[-1].endswith(" list")
    assert route("sharepoint", *try_lines[-1].split()[2:]) is not None


def test_help_is_the_same_page_as_the_bare_node(web: str, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["help", "sharepoint", "web"]) == 0
    printed = capsys.readouterr().out

    assert printed.rstrip("\n") == web
    # The audience word may stand in for the product, which is how `o365 help sharepoint web`
    # and `o365 help graph directory user` are the same request.
    assert main(["help", "directory", "user"]) == 0
    assert "directory user — User" in capsys.readouterr().out


def test_help_for_a_leaf_prints_the_flags_of_the_method_it_reached(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["help", "sharepoint", "web", "lists", "list"]) == 0
    printed = capsys.readouterr().out

    assert printed.startswith("usage: o365 sharepoint web lists list")
    for flag in ("-o", "--columns", "--link", "--no-headers"):
        assert flag in printed
    # The formats are the renderer's, so `-h` cannot drift from what `-o` accepts.
    from office365.runtime.render import FORMATS

    assert "{" + ",".join(FORMATS) + "}" in printed


def test_a_graph_noun_is_refused_by_naming_the_products_that_serve_it(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["graph", "user"]) == REFUSED
    printed = capsys.readouterr().err

    assert "graph is a token, not a product" in printed
    assert "directory" in printed


def test_an_action_sentence_is_the_services_own_summary() -> None:
    from office365.directory.users.user import User
    from office365.runtime.verbs import verbs_of

    verbs = verbs_of(User)
    name = next(name for name, meta in verbs.items() if meta.role == "action" and meta.expose)
    sentence = _sentence(User, name, verbs[name])

    assert sentence
    assert not sentence.endswith(".")
    assert "Requires permissions" not in sentence

    # A docstring that opens with a block header has no summary, and says so by saying nothing.
    assert _sentence(User, "export_device_and_app_management_data", verbs["export_device_and_app_management_data"]) == ""


def test_a_type_with_actions_shows_them_with_the_metadata_summary(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["help", "directory", "user"]) == 0
    printed = capsys.readouterr().out

    assert "READ\n" in printed and "  get  " in printed
    assert "  list  " in printed
    assert "Assign a license" not in printed  # the sentence belongs to `assign-license`, not the page's top
    assert "read this one back" in printed


class _Row:
    """One item of a feed: a payload, and the REST address the item was read from."""

    def __init__(self, title: str, address: "str | None" = None) -> None:
        self.title = title
        self.resource_url = address

    def to_json(self) -> dict:
        return {"displayName": self.title, "webUrl": f"https://contoso.example/{self.title}"}


class _Feed:
    """A collection as the runtime hands it over: iterable over items, JSON of many rows."""

    def __init__(self, rows: "list[_Row]") -> None:
        self.query_options = QueryOptions()
        self.rows = rows
        self.selected: "list[str]" = []

    def __iter__(self):
        return iter(self.rows)

    def item_type(self):
        return _Row

    def select(self, names):
        self.selected = list(names)
        return self

    def to_json(self) -> "list[dict]":
        return [row.to_json() for row in self.rows]


class _Object:
    """One entity as the runtime hands it over: iterable over its own fields, JSON of one row."""

    def __init__(self, payload: "dict") -> None:
        self.payload = payload
        self.query_options = QueryOptions()

    def __iter__(self):
        return iter([(name, value, False) for name, value in self.payload.items()])

    def to_json(self) -> "dict":
        return dict(self.payload)


class _Client:
    """Just enough client: the command calls the one query the method queued."""

    service_root_url = "https://contoso.sharepoint.com/sites/x/_api/"

    def __init__(self) -> None:
        self.queried = 0

    def execute_query(self) -> None:
        self.queried += 1


def _arguments(link: str = "auto", output: str = "table", columns: "str | None" = None) -> "argparse.Namespace":
    return argparse.Namespace(output=output, columns=columns, link=link, no_headers=False)


def test_a_feed_is_one_row_per_item_and_each_row_keeps_its_own_address(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.teams.team import Team

    rows = [_Row("alpha", "https://contoso.example/alpha"), _Row("beta", "https://contoso.example/beta")]
    sent = _send(_Client(), lambda **given: _Feed(rows), {}, _arguments("always"), Team)

    lines = capsys.readouterr().out.splitlines()
    assert sent == 0
    assert lines[0].split() == ["DISPLAYNAME", "WEBURL"]
    assert len(lines) == HEADER_AND_TWO_ROWS
    # The address of each row is in that row's line, not in the first line twice.
    assert "https://contoso.example/alpha" in lines[1]
    assert "https://contoso.example/beta" in lines[2]


def test_a_row_with_no_address_does_not_shift_the_next_rows_link(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.teams.team import Team

    rows = [_Row("alpha"), _Row("beta", "https://contoso.example/beta")]
    _send(_Client(), lambda **given: _Feed(rows), {}, _arguments("always"), Team)

    lines = capsys.readouterr().out.splitlines()
    assert "contoso.example/beta" in lines[2]
    assert "contoso.example/beta" not in lines[1]


def test_a_feed_with_fewer_addresses_than_rows_still_prints(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.runtime.render import render

    printed = render([{"a": 1}, {"a": 2}], resources=["https://contoso.example/one"])

    assert printed.splitlines() == ["A", "1", "2"]
    assert capsys.readouterr().out == ""


def test_a_result_whose_json_is_a_table_is_already_rows(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.teams.team import Team

    class _Report:
        """``Report`` answers a CSV as JSON: the payload *is* the table, so it is not one row."""

        def to_json(self) -> "list[dict]":
            return [{"displayName": "alpha"}, {"displayName": "beta"}]

    _send(_Client(), lambda **given: _Report(), {}, _arguments(), Team)

    # The ranked `displayName` column is the one these rows carry; `webUrl` is absent, so is not a column.
    assert [line.strip() for line in capsys.readouterr().out.splitlines()] == ["DISPLAYNAME", "alpha", "beta"]


def test_a_table_asks_the_service_for_the_columns_it_prints(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.teams.team import Team

    feed = _Feed([_Row("alpha", "https://contoso.example/alpha")])
    _send(_Client(), lambda **given: feed, {}, _arguments(), Team)

    # `/Web/lists` answers without its address unless it is selected, so the request names both:
    # the ranked columns a table prints, then the field the row links to.
    assert feed.selected == ["displayName", "webUrl"]
    capsys.readouterr()


def test_json_takes_whatever_the_service_sends(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.teams.team import Team

    feed = _Feed([_Row("alpha", "https://contoso.example/alpha")])
    _send(_Client(), lambda **given: feed, {}, _arguments(output="json"), Team)

    # A caller piping to jq is reading the service, not our idea of a table.
    assert feed.selected == []
    capsys.readouterr()


def test_named_columns_are_the_ones_asked_for(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.teams.team import Team

    feed = _Feed([_Row("alpha", "https://contoso.example/alpha")])
    _send(_Client(), lambda **given: feed, {}, _arguments(columns="displayName"), Team)

    # What was named, then the address: a link that costs nothing to ask for.
    assert feed.selected == ["displayName", "webUrl"]
    capsys.readouterr()


def test_one_object_is_a_block_of_fields_not_a_row_per_field(capsys: pytest.CaptureFixture[str]) -> None:
    from office365.cli import _send
    from office365.sharepoint.webs.web import Web

    payload = {"Title": "SiteU74H3Z9O", "Url": "https://mediadev8.sharepoint.com"}
    _send(_Client(), lambda **given: _Object(payload), {}, _arguments(), Web)

    # An entity iterates its fields as `(name, value, stated)` triples -- that is what a request
    # carries -- so iterating one printed `["Title", "SiteU74H3Z9O", false]` under a `VALUE`
    # heading. One object is one block, and each field is on its own line, name first.
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].split() == ["Title", "SiteU74H3Z9O"]
    assert lines[1].split() == ["Url", "https://mediadev8.sharepoint.com"]
    assert "VALUE" not in "\n".join(lines)
