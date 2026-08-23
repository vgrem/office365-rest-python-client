"""Offline unit tests for response parsing (no credentials)."""

from __future__ import annotations

import unittest

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_result import ClientResult
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.client_context import ClientContext
from requests import Response
from tests import test_site_url


class TestResponseParsing(unittest.TestCase):
    """A malformed body must surface as ClientRequestException, not ValueError."""

    def test_malformed_json_raises_client_request_exception(self):
        ctx = ClientContext(test_site_url)
        request = ODataRequest(test_site_url, JsonLightFormat())
        query = ClientQuery(ctx, return_type=ClientResult(ctx))

        resp = Response()
        resp.status_code = 200
        resp.url = f"{test_site_url}/_api/web"
        resp.headers["Content-Type"] = "application/json"
        resp._content = b"<html><body>Expired form digest</body></html>"

        with self.assertRaises(ClientRequestException) as cm:
            request.process_response(resp, query)

        self.assertIs(cm.exception.response, resp)

    def test_raw_content_query_returns_bytes_for_json(self):
        """A raw-content query (e.g. OneDrive /content) must return bytes even when the
        downloaded file is JSON and the server reports application/json."""
        ctx = ClientContext(test_site_url)
        request = ODataRequest(test_site_url, JsonLightFormat())
        result = ClientResult(ctx, bytes())
        query = FunctionQuery(ctx.web, "content", return_type=result, return_raw_content=True)

        resp = Response()
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/json"
        resp._content = b'{"name": "test", "version": 1}'

        request.process_response(resp, query)
        self.assertEqual(result.value, b'{"name": "test", "version": 1}')

    def test_regular_query_still_parses_json(self):
        """Without the raw-content flag, application/json is still parsed as OData JSON."""
        ctx = ClientContext(test_site_url)
        request = ODataRequest(test_site_url, JsonLightFormat())
        result = ClientResult(ctx)
        query = FunctionQuery(ctx.web, "content", return_type=result)

        resp = Response()
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/json"
        resp._content = b'{"name": "test", "version": 1}'

        request.process_response(resp, query)
        self.assertIsNot(result.value, b'{"name": "test", "version": 1}')

    def test_raw_content_returns_bytes_for_octet_stream(self):
        """Non-JSON content types keep returning raw bytes without the flag."""
        ctx = ClientContext(test_site_url)
        request = ODataRequest(test_site_url, JsonLightFormat())
        result = ClientResult(ctx, bytes())
        query = FunctionQuery(ctx.web, "$value", return_type=result)

        resp = Response()
        resp.status_code = 200
        resp.headers["Content-Type"] = "application/octet-stream"
        resp._content = b"\x00\x01\x02"

        request.process_response(resp, query)
        self.assertEqual(result.value, b"\x00\x01\x02")
