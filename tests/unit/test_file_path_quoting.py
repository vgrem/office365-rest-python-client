"""Offline tests for apostrophe escaping in File.read()/write() paths (refs issue #884)."""

from __future__ import annotations

import unittest

from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from requests import Response
from tests import test_site_url


class _CaptureTransport(BaseTransport):
    def __init__(self):
        super().__init__()
        self.url = ""

    def execute(self, request):
        self.url = request.url
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp.headers["Content-Type"] = "application/octet-stream"
        resp._content = b"payload"
        return resp


class TestFilePathQuoting(unittest.TestCase):
    """Apostrophes in server-relative paths must be escaped in the DecodedUrl literal."""

    def _context(self) -> tuple[ClientContext, _CaptureTransport]:
        ctx = ClientContext(test_site_url)
        transport = _CaptureTransport()
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = transport
        return ctx, transport

    def test_read_escapes_apostrophe(self):
        ctx, transport = self._context()
        result = File.open_binary(ctx, "/sites/x/Shared Documents/macdonald's file.txt")

        self.assertEqual(result.content, b"payload")
        self.assertIn("getFileByServerRelativePath", transport.url)
        self.assertIn("macdonald%27%27s", transport.url)

    def test_read_with_plain_path_unchanged(self):
        ctx, transport = self._context()
        result = File.open_binary(ctx, "/sites/x/Shared Documents/report.pdf")

        self.assertEqual(result.content, b"payload")
        self.assertIn("report.pdf", transport.url)
        self.assertNotIn("%27%27", transport.url)

    def test_write_escapes_apostrophe(self):
        ctx, transport = self._context()
        result = File.save_binary(ctx, "/sites/x/macdonald's file.txt", b"content")

        self.assertEqual(result.status_code, 200)
        self.assertIn("macdonald%27%27s", transport.url)


if __name__ == "__main__":
    unittest.main()
