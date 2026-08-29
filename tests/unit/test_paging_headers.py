"""Offline tests for server-driven paging: custom headers preserved across pages."""

from __future__ import annotations

import json as jsonlib
import unittest
from types import SimpleNamespace

from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.transport.base import BaseTransport
from requests import Response

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


if __name__ == "__main__":
    unittest.main()
