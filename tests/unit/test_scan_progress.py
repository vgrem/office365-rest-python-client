"""Offline tests for progress hooks on recursive scan operations (get_files/get_folders/get_all_webs)."""

from __future__ import annotations

import json as jsonlib
import unittest

from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from requests import Response

_METADATA = {"__metadata": {"type": "SP.Folder"}}


def _web(url: str) -> dict:
    return {"__metadata": {"type": "SP.Web"}, "Url": url}


def _files_result(urls: list[str]) -> dict:
    return {"d": {"results": [{"__metadata": {"type": "SP.File"}, "ServerRelativeUrl": u} for u in urls]}}


def _folders_result(urls: list[str]) -> dict:
    return {"d": {"results": [{**_METADATA, "ServerRelativeUrl": u} for u in urls]}}


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


class TestScanProgress(unittest.TestCase):
    def _context(self, transport: _ScriptedTransport) -> ClientContext:
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()  # no auth handler during offline build
        ctx.pending_request().transport = transport
        return ctx

    def test_get_files_progress_fires_once(self):
        ctx = self._context(_ScriptedTransport([_files_result(["/a.txt", "/b.txt"])]))
        seen = []
        folder = ctx.web.get_folder_by_server_relative_url("Shared Documents")

        folder.get_files(False, progress=seen.append).execute_query()

        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0].done, 2)  # noqa: PLR2004
        self.assertEqual(seen[0].stage, "scanning")
        self.assertEqual([f.server_relative_url for f in (seen[0].items or [])], ["/a.txt", "/b.txt"])

    def test_get_folders_progress_fires_once(self):
        ctx = self._context(_ScriptedTransport([_folders_result(["/sub"])]))
        seen = []
        folder = ctx.web.get_folder_by_server_relative_url("Shared Documents")

        folder.get_folders(False, progress=seen.append).execute_query()

        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0].done, 1)
        self.assertEqual(len(seen[0].items or []), 1)

    def test_get_files_recursive_fires_per_folder(self):
        payloads = [
            _files_result(["/a.txt", "/b.txt"]),  # root folder's files
            _folders_result(["/sub"]),  # root folder's sub-folders
            _files_result(["/sub/c.txt"]),  # the sub-folder's files
            _folders_result([]),  # the sub-folder has no further sub-folders
        ]
        ctx = self._context(_ScriptedTransport(payloads))
        seen = []
        folder = ctx.web.get_folder_by_server_relative_url("Shared Documents")

        folder.get_files(True, progress=seen.append).execute_query()

        # root scan then the sub-folder scan, with cumulative done
        self.assertEqual([p.done for p in seen], [2, 3])  # noqa: PLR2004
        self.assertEqual([f.server_relative_url for f in (seen[-1].items or [])], ["/sub/c.txt"])

    def test_get_files_forward_select(self):
        """Fluent .select() on get_files is forwarded to the file collection GET."""
        urls = []

        class _CaptureTransport(_ScriptedTransport):
            def execute(self, request):
                urls.append(request.url)
                return super().execute(request)

        ctx = self._context(_CaptureTransport([_files_result(["/a.txt"])]))
        folder = ctx.web.get_folder_by_server_relative_url("Shared Documents")

        result = folder.get_files(False)
        result.select(["Name"])
        result.execute_query()

        self.assertTrue(any("$select=" in url and "Name" in url and "ServerRelativeUrl" in url for url in urls))

    def test_get_all_webs_progress_fires_per_web(self):
        payloads = [
            {"d": {"Webs": {"results": [_web("https://x/sub1"), _web("https://x/sub2")]}}},
            {"d": {"Webs": {"results": []}}},
            {"d": {"Webs": {"results": []}}},
        ]
        ctx = self._context(_ScriptedTransport(payloads))
        seen = []

        ctx.web.get_all_webs(progress=seen.append).execute_query()

        self.assertEqual([p.done for p in seen], [1, 2])  # noqa: PLR2004

    def test_progress_items_is_optional(self):
        from office365.runtime.operations import Progress

        self.assertIsNone(Progress(done=5).items)  # noqa: PLR2004
        self.assertIsNotNone(Progress(done=5, items=[1, 2]).items)  # noqa: PLR2004


def _nav_node(node_id: int, title: str, url: str) -> dict:
    return {"__metadata": {"type": "SP.NavigationNode"}, "Id": node_id, "Title": title, "Url": url}


class TestNavigationGetAll(unittest.TestCase):
    _PAYLOADS = [
        {"d": {"results": [_nav_node(1, "Home", "/"), _nav_node(2, "About", "/about")]}},
        {"d": {"results": []}},  # Home.children
        {"d": {"results": [_nav_node(3, "Team", "/about/team")]}},  # About.children
        {"d": {"results": []}},  # Team.children
    ]

    def _walk(self, progress=None) -> tuple[list, list]:
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
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

    def test_to_json_nests_children(self):
        nodes, _ = self._walk()
        tree = nodes.to_json()
        by_title = {t.get("Title"): t for t in tree}
        self.assertEqual(by_title["About"]["Children"][0]["Title"], "Team")
        self.assertEqual(by_title["About"]["Children"][0]["Children"], [])
        self.assertEqual(by_title["Home"]["Children"], [])


if __name__ == "__main__":
    unittest.main()
