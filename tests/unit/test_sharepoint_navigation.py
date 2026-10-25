"""Offline tests for best-effort web navigation replication.

The item adapters carry content; ``navigation.py`` copies a web's Quick Launch and
top navigation bar. A node is the model — ``NavigationNode`` with its
``Children`` — so these tests build the real objects over a context that answers a
read from memory and counts every request instead of sending one. They assert that
missing nodes are created with rewritten links, existing nodes are reconciled
rather than duplicated, URL-less (dynamic) nodes are skipped with a warning, and a
web that inherits its navigation only flips the target's ``use_shared`` flag.

The create body itself is pinned in ``tests/unit/test_navigation_node_create.py``;
the library read that fills the tree, in ``tests/unit/test_navigation_tree.py``.
"""

from __future__ import annotations

from office365.migration.sharepoint.navigation import (
    apply_navigation,
    capture_navigation,
    verify_navigation,
)
from office365.sharepoint.navigation.navigation import Navigation
from office365.sharepoint.navigation.nodes.node import NavigationNode

_SOURCE = "https://mediadev8.sharepoint.com/sites/team_in"
_TARGET = "https://mediadev8.sharepoint.com/sites/team_out"


class _Context:
    """Enough of a context to build a model on: every execution is counted, none sent."""

    def __init__(self) -> None:
        self.executed = 0
        self._after = []

    def add_query(self, query):
        return self

    def load(self, client_object, properties_to_retrieve=None):
        return self  # a read is queued, and answered from memory when it executes

    def after_execute(self, action, *args, **kwargs):
        self._after.append(action)  # the read is answered from memory, so the hook fires locally
        return self

    def execute_query(self):
        self.executed += 1
        while self._after:
            self._after.pop(0)(None)
        return self


class _Loaded:
    """An already-materialized collection: a read makes no request, a create queues none."""

    def __init__(self, items=()) -> None:
        self.items = list(items)

    def get(self):
        return self

    def get_all_nodes(self, recursive: bool = True, progress=None):
        return self  # already materialized: the walk is ``NavigationNodeCollection.get_all_nodes``

    def execute_query(self):
        return self

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def add(self, info):
        node = NavigationNode(_Context())  # its own context: materializing it is not the web's flush
        node.set_property("Title", info.Title)
        node.set_property("Url", info.Url)
        node.set_property("Children", _Loaded())
        self.items.append(node)
        return node


class _Web:
    """A web whose navigation is the real model, over a context that sends nothing."""

    def __init__(self, url: str, *, use_shared: bool = False, quick_launch=(), top=()) -> None:
        self.url = url
        self.context = _Context()
        navigation = Navigation(self.context)
        navigation.set_property("UseShared", use_shared)
        navigation.set_property("QuickLaunch", _Loaded(quick_launch))
        navigation.set_property("TopNavigationBar", _Loaded(top))
        self.navigation = navigation

    @property
    def use_shared(self):
        return self.navigation.use_shared


def _node(title: str, url: str, children=()) -> NavigationNode:
    node = NavigationNode(_Context())
    node.set_property("Title", title)
    node.set_property("Url", url)
    node.set_property("Children", _Loaded(children))
    return node


def _source_web():
    custom = _node("Wiki", "/sites/team_in/Pages/Wiki.aspx", [_node("Sub", "https://intranet.example.com")])
    recent = _node("Recent", "", [_node("Depts", "/sites/team_in/Lists/Depts/AllItems.aspx")])
    quick_launch = [
        _node("Home", "/sites/team_in"),
        recent,
        _node("Recent-ish", "/sites/team_in/Shared Documents"),
        custom,
    ]
    return _Web(_SOURCE, quick_launch=quick_launch)


def _target_web():
    return _Web(_TARGET, quick_launch=[_node("Home", "/sites/team_out"), _node("Recent", "")])


def test_capture_is_the_models_own_tree_in_both_bars():
    captured = capture_navigation(_source_web())

    assert [n.title for n in captured.quick_launch] == ["Home", "Recent", "Recent-ish", "Wiki"]
    assert captured.top_navigation_bar is not None
    wiki = captured.quick_launch[3]
    assert [c.title for c in wiki.children] == ["Sub"]
    # the whole tree is read, the dynamic node's computed children included
    assert [c.title for c in captured.quick_launch[1].children] == ["Depts"]
    assert isinstance(captured, Navigation)


def test_apply_creates_missing_nodes_with_rewritten_links():
    source, target = _source_web(), _target_web()

    warnings: list[str] = []
    apply_navigation(source, target, warnings)

    # one read of the target's navigation, one flush of the creates it queued
    reads_and_flushes = 2
    assert target.context.executed == reads_and_flushes
    created = {n.title: n for n in target.navigation.get().execute_query().quick_launch}
    assert created["Wiki"].url == "/sites/team_out/Pages/Wiki.aspx"
    assert [c.title for c in created["Wiki"].children] == ["Sub"]
    assert created["Wiki"].children[0].url == "https://intranet.example.com"
    # the dynamic node is skipped and reported, never created
    assert "Recent" in created and created["Recent"].url == ""
    assert any("Recent" in w and "no URL" in w for w in warnings)
    # Home already existed by title, so it is neither re-created nor rewritten
    assert created["Home"].url == "/sites/team_out"


def test_verify_reports_missing_and_mismatched_nodes_and_is_clean_when_replicated():
    source, target = _source_web(), _target_web()

    assert any("Wiki" in i and "not created" in i for i in verify_navigation(source, target))

    apply_navigation(source, target, [])
    assert verify_navigation(source, target) == []

    target.navigation.get().execute_query().quick_launch[0].url = "/sites/team_out/Elsewhere"
    assert any("Home" in i and "expected" in i for i in verify_navigation(source, target))


def test_a_web_that_inherits_only_flips_the_targets_flag():
    source = _Web(_SOURCE, use_shared=True, quick_launch=[_node("Home", "/sites/team_in")])
    target = _target_web()

    apply_navigation(source, target, [])

    assert target.use_shared is True
    assert [n.title for n in target.navigation.get().execute_query().quick_launch] == ["Home", "Recent"]
    assert verify_navigation(source, target) == []
