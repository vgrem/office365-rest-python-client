"""A recursive navigation walk visits every node once, carrying progress as it goes."""

import json as jsonlib
import unittest

from office365.migration.offline import offline_sharepoint_context
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.nodes.collection import NavigationNodeCollection
from requests import Response


class _ScriptedTransport(BaseTransport):
    def __init__(self, payloads: list[dict]) -> None:
        self._payloads = payloads
        self.calls = 0

    def execute(self, request):
        payload = self._payloads[min(self.calls, len(self._payloads) - 1)]
        self.calls += 1
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp.headers.update({"Content-Type": "application/json;odata=verbose"})
        resp._content = jsonlib.dumps(payload).encode("utf-8")
        return resp


def _nav_node(node_id: int, title: str, url: str) -> dict:
    return {"__metadata": {"type": "SP.NavigationNode"}, "Id": node_id, "Title": title, "Url": url}


class TestNavigationGetAll(unittest.TestCase):
    """``get_all_nodes(recursive=True)`` is a tree walk, not a page read.

    The payloads are one page per collection, so "every node once, in order" is the
    property under test -- a walk that revisited a parent would ask for more pages than
    there are, and ``progress`` would count a node twice.
    """

    _PAYLOADS = [
        {"d": {"results": [_nav_node(1, "Home", "/"), _nav_node(2, "About", "/about")]}},
        {"d": {"results": []}},  # Home.children
        {"d": {"results": [_nav_node(3, "Team", "/about/team")]}},  # About.children
        {"d": {"results": []}},  # Team.children
    ]

    def _walk(self, progress=None) -> tuple[NavigationNodeCollection, list]:
        ctx: ClientContext = offline_sharepoint_context()
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = _ScriptedTransport(self._PAYLOADS)
        seen = []
        hook = progress or seen.append
        nodes = ctx.web.navigation.top_navigation_bar.get_all_nodes(recursive=True, progress=hook).execute_query()
        return nodes, seen

    def test_get_all_walks_all_nodes(self):
        nodes, seen = self._walk()
        self.assertEqual([n.get_property("Title") for n in nodes], ["Home", "About", "Team"])
        self.assertEqual([p.done for p in seen], [1, 2, 3])  # noqa: PLR2004


if __name__ == "__main__":
    unittest.main()
