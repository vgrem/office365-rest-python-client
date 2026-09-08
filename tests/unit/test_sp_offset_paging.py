"""Offline tests for SharePoint client-driven (offset) paging fallback (refs issue #915)."""

from __future__ import annotations

import unittest

from office365.sharepoint.client_context import ClientContext
from tests import test_site_url
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport


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


if __name__ == "__main__":
    unittest.main()
