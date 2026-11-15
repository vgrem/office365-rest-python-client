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

import pytest
from office365.cli import _page, _sentence, main
from office365.routing import route

#: A page wraps its links and stops; six lines is the twelve words plus the "and N more" line.
PAGE_LINK_LINES = 6
#: What ``main`` returns for a word it refuses.
REFUSED = 2


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
