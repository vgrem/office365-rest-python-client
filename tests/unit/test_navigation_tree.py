"""Offline tests for ``Navigation.get_tree()`` — both bars, whole tree, one execution.

A navigation read returns its two bars as navigations, so each property builds a fresh
collection per access and the read that fills one is not the read a caller walks.
``get_tree()`` expands both bars so the response carries them as the model's own
collections, then walks them with ``NavigationNodeCollection.get_all_nodes``. The
transport answers those requests by URL, so the assertions are about one
``execute_query()`` and the tree it leaves behind.
"""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.navigation import Navigation
from tests._scripted_transport import MethodRoutingTransport


def _node(node_id: int, title: str, url: str) -> dict:
    return {"__metadata": {"type": "SP.NavigationNode"}, "Id": node_id, "Title": title, "Url": url}


_NAVIGATION = {
    "d": {
        "__metadata": {"type": "SP.Navigation"},
        "UseShared": False,
        "QuickLaunch": {"results": [_node(1, "Home", "/")]},
        "TopNavigationBar": {"results": [_node(2, "About", "/about")]},
    }
}

_ROUTES = [
    # a leaf answers with no children; most specific first, because a child's URL
    # contains its parent's (``/QuickLaunch(1)/Children(3)/Children``)
    ("GET", "Children(3)/Children", {"d": {"results": []}}),
    ("GET", "QuickLaunch(1)/Children", {"d": {"results": [_node(3, "Team", "/team")]}}),
    ("GET", "TopNavigationBar(2)/Children", {"d": {"results": []}}),
    ("GET", "/Navigation", _NAVIGATION),
]


def test_get_tree_expands_both_bars_and_walks_every_level_in_one_execution():
    transport = MethodRoutingTransport(_ROUTES)
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    ctx.pending_request().beforeExecute.clear()  # no auth handler when nothing leaves the process
    ctx.pending_request().transport = transport

    navigation = ctx.web.navigation.get_tree().execute_query()

    assert isinstance(navigation, Navigation)  # the model, not a flat copy of it
    assert navigation.use_shared is False
    assert [n.title for n in navigation.quick_launch] == ["Home"]
    assert [n.title for n in navigation.quick_launch[0].children] == ["Team"]  # a level below the bar
    assert [n.title for n in navigation.top_navigation_bar] == ["About"]
    # one navigation read (both bars expanded) + one child read per node that has any
    expected_requests = 4
    assert len(transport.requests) == expected_requests
