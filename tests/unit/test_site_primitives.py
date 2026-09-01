"""Offline tests for the migration-supporting site primitives.

Covers the accessors added/cleaned up for the assessment scans:
``Web.site_id``, ``Site.get_storage_metrics()``, and the ``None`` missing-value
sentinels on ``LastItem*Date`` (no more naive ``datetime.min``).
"""

from __future__ import annotations

import json as jsonlib
import unittest

from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from requests import Response


class _ScriptedTransport(BaseTransport):
    def __init__(self, payloads: list) -> None:
        self._payloads = payloads
        self.calls = 0

    def execute(self, request):
        payload = self._payloads[self.calls]
        self.calls += 1
        resp = Response()
        resp.url = request.url
        resp.status_code = 200
        resp.headers.update({"Content-Type": "application/json;odata=verbose"})
        resp._content = jsonlib.dumps(payload).encode("utf-8")
        return resp


def _ctx(payloads: list) -> ClientContext:
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = _ScriptedTransport(payloads)
    return ctx


class TestSitePrimitives(unittest.TestCase):
    def test_web_site_id(self):
        ctx = _ctx([{"d": {"__metadata": {"type": "SP.Web"}, "Id": "web-1", "SiteId": "site-1", "Url": "https://x"}}])
        web = ctx.web.get().execute_query()
        self.assertEqual(web.site_id, "site-1")
        self.assertEqual(web.id, "web-1")

    def test_site_get_storage_metrics(self):
        ctx = _ctx([{"d": {"TotalSize": 644245094400, "TotalFileCount": 120, "VersionCount": 12}}])
        metrics = ctx.site.get_storage_metrics().execute_query()
        self.assertEqual(metrics.total_size, 644245094400)  # noqa: PLR2004
        self.assertEqual(metrics.total_file_count, 120)  # noqa: PLR2004
        self.assertEqual(metrics.version_count, 12)  # noqa: PLR2004

    def test_list_last_item_modified_date_none_when_absent(self):
        ctx = _ctx(
            [
                {
                    "d": {
                        "results": [
                            {"__metadata": {"type": "SP.List"}, "Id": "1", "Title": "A", "Hidden": False},
                            {
                                "__metadata": {"type": "SP.List"},
                                "Id": "2",
                                "Title": "B",
                                "Hidden": False,
                                "LastItemModifiedDate": "2024-01-02T03:04:05Z",
                            },
                        ]
                    }
                }
            ]
        )
        lists = ctx.web.lists.get().execute_query()
        self.assertIsNone(lists[0].last_item_modified_date)
        self.assertIsNotNone(lists[1].last_item_modified_date)
        self.assertEqual(lists[1].last_item_modified_date.year, 2024)  # noqa: PLR2004

    def test_web_last_item_modified_date_none_when_absent(self):
        ctx = _ctx([{"d": {"__metadata": {"type": "SP.Web"}, "Url": "https://x"}}])
        web = ctx.web.get().execute_query()
        self.assertIsNone(web.last_item_modified_date)


if __name__ == "__main__":
    unittest.main()
