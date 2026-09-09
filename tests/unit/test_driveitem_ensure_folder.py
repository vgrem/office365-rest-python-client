"""Offline tests for DriveItem.ensure_folder (refs issue #862)."""

from __future__ import annotations

import json
import unittest

from office365.graph_client import GraphClient
from office365.runtime.transport.base import BaseTransport
from requests import Response


def _item(item_id: str, name: str) -> dict:
    return {"id": item_id, "name": name, "folder": {}, "@odata.type": "#microsoft.graph.driveItem"}


def _not_found() -> dict:
    return {"error": {"code": "itemNotFound", "message": "Item not found"}}


class _CaptureTransport(BaseTransport):
    def __init__(self, responses: list[tuple[int, dict]]):
        super().__init__()
        self._responses = responses
        self.urls: list[str] = []

    def execute(self, request):
        status, body = self._responses.pop(0)
        self.urls.append(request.url)
        resp = Response()
        resp.status_code = status
        resp.url = request.url
        resp.headers["Content-Type"] = "application/json"
        resp._content = json.dumps(body).encode()
        return resp


class TestDriveItemEnsureFolder(unittest.TestCase):
    def _client(self) -> tuple[GraphClient, _CaptureTransport]:
        client = GraphClient()
        transport = _CaptureTransport(
            [
                (404, _not_found()),  # GET a
                (201, _item("a1", "a")),  # POST a
                (200, _item("a1", "a")),  # GET a (reload)
                (404, _not_found()),  # GET a/b
                (201, _item("b2", "b")),  # POST b
                (200, _item("b2", "b")),  # GET a/b (reload)
                (404, _not_found()),  # GET a/b/c
                (201, _item("c3", "c")),  # POST c
                (200, _item("c3", "c")),  # GET a/b/c (reload)
            ]
        )
        client.pending_request().beforeExecute.clear()
        client.pending_request().transport = transport
        return client, transport

    def test_creates_missing_nested_folders(self):
        client, transport = self._client()

        target = client.me.drive.root.ensure_folder("a/b/c")
        client.execute_query()

        posts = [url for url in transport.urls if "children" in url]
        self.assertEqual(len(posts), 3)  # noqa: PLR2004
        self.assertEqual(target.get_property("id"), "c3")
        self.assertEqual(target.get_property("name"), "c")


if __name__ == "__main__":
    unittest.main()
