"""Offline unit tests for response parsing (no credentials)."""

from __future__ import annotations

import unittest

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_result import ClientResult
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.queries.client_query import ClientQuery
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
