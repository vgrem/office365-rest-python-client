"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import json as jsonlib
import unittest
from types import SimpleNamespace

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from requests import Response
from tests import test_site_url
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport

NEXT_LINK = "https://graph.microsoft.com/v1.0/users?$skiptoken=abc"

PAGE_1_HEADERS = {
    "Authorization": "Bearer real",
    "ConsistencyLevel": "eventual",
    "X-Custom": "1",
    "Content-Length": "42",
}


class _FakeTransport(BaseTransport):
    def __init__(self) -> None:
        self.requests: list = []

    def execute(self, request):
        self.requests.append(request)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp.headers.update({"Content-Type": "application/json"})
        resp._content = jsonlib.dumps({"@odata.nextLink": NEXT_LINK, "value": []}).encode("utf-8")
        resp.request = SimpleNamespace(headers=dict(PAGE_1_HEADERS))
        return resp


def _page1(col: ClientObjectCollection) -> _FakeTransport:
    client = col.context
    client.pending_request().beforeExecute.clear()  # no auth handler during offline build
    transport = _FakeTransport()
    client.pending_request().transport = transport
    col.paged(10).get().execute_query()
    return transport


class TestPagingHeaders(unittest.TestCase):
    def test_first_page_captures_headers_and_next_link(self):
        client = GraphClient()
        col = ClientObjectCollection(client, User, ResourcePath("users"))
        _page1(col)

        self.assertEqual(col._next_request_url, NEXT_LINK)
        self.assertEqual(col._page_headers, PAGE_1_HEADERS)

    def test_next_page_reapplies_custom_headers(self):
        client = GraphClient()
        col = ClientObjectCollection(client, User, ResourcePath("users"))
        transport = _page1(col)

        col._get_next()
        col.execute_query()

        request = transport.requests[-1]
        self.assertEqual(request.url, NEXT_LINK)
        self.assertEqual(request.headers.get("ConsistencyLevel"), "eventual")
        self.assertEqual(request.headers.get("X-Custom"), "1")

    def test_next_page_skips_auth_and_content_length(self):
        client = GraphClient()
        col = ClientObjectCollection(client, User, ResourcePath("users"))
        transport = _page1(col)

        col._get_next()
        col.execute_query()

        headers = {k.lower(): v for k, v in transport.requests[-1].headers.items()}
        self.assertNotIn("authorization", headers)
        self.assertNotIn("content-length", headers)

    def test_get_next_without_token_raises(self):
        client = GraphClient()
        col = ClientObjectCollection(client, User, ResourcePath("users"))
        with self.assertRaises(ValueError):
            col._get_next()


def _page(items: list) -> dict:
    return {"d": {"results": [{"Id": str(i), "Title": f"List {i}"} for i in items]}}


class _CaptureTransport(_ScriptedTransport):
    def __init__(self, payloads):
        super().__init__(payloads)
        self.urls: list[str] = []

    def execute(self, request):
        self.urls.append(request.url)
        return super().execute(request)


class TestSPOffsetPaging(unittest.TestCase):
    """When a SharePoint endpoint returns no __next link, paged(page_size) falls back to $skip."""

    def _context(self, payloads: list) -> tuple[ClientContext, _CaptureTransport]:
        ctx = ClientContext(test_site_url)
        transport = _CaptureTransport(payloads)
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = transport
        return ctx, transport

    def test_paged_falls_back_to_skip_paging(self):
        ctx, transport = self._context([_page([1, 2]), _page([3, 4]), _page([])])
        pages = ctx.web.lists.paged(2).get().execute_query()

        items = list(pages)

        self.assertEqual(len(items), 4)  # noqa: PLR2004
        self.assertEqual(transport.calls, 3)  # noqa: PLR2004
        self.assertIn("skip=2", transport.urls[1])
        self.assertIn("skip=4", transport.urls[2])

    def test_paged_stops_on_short_page(self):
        ctx, transport = self._context([_page([1, 2]), _page([3])])
        pages = ctx.web.lists.paged(2).get().execute_query()

        items = list(pages)

        self.assertEqual(len(items), 3)  # noqa: PLR2004
        self.assertEqual(transport.calls, 2)  # noqa: PLR2004
        self.assertIn("skip=2", transport.urls[1])

    def test_full_final_page_issues_one_empty_request(self):
        ctx, transport = self._context([_page([1, 2]), _page([3, 4]), _page([])])
        pages = ctx.web.lists.paged(2).get().execute_query()

        self.assertEqual(len(pages), 2)  # noqa: PLR2004
        self.assertTrue(pages.has_next)

        items = list(pages)

        self.assertEqual(len(items), 4)  # noqa: PLR2004
        self.assertEqual(transport.calls, 3)  # noqa: PLR2004
