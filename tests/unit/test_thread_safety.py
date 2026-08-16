"""Offline tests for the concurrency prerequisites (single-flight caches, batch pre-split)."""

from __future__ import annotations

import threading
import time
import unittest
from unittest import mock

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.request import SharePointRequest
from office365.sharepoint.webs.context_web_information import ContextWebInformation


def _run_concurrently(target, count: int = 2) -> None:
    barrier = threading.Barrier(count)

    def _wrapped():
        barrier.wait()
        target()

    threads = [threading.Thread(target=_wrapped) for _ in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


class TestThreadSafety(unittest.TestCase):
    def test_with_access_token_single_flight(self):
        auth_ctx = AuthenticationContext("https://contoso.sharepoint.com")
        calls: list[int] = []

        def token_func():
            calls.append(1)
            time.sleep(0.1)
            return {"accessToken": "token", "tokenType": "Bearer", "expiresIn": 3600}

        auth_ctx.with_access_token(token_func)

        def _authenticate():
            auth_ctx.authenticate_request(RequestOptions("https://contoso.sharepoint.com"))

        _run_concurrently(_authenticate)

        self.assertEqual(len(calls), 1)

    def test_ensure_form_digest_single_flight(self):
        request = SharePointRequest("https://contoso.sharepoint.com")
        context_info = ContextWebInformation(
            FormDigestValue="digest",
            FormDigestTimeoutSeconds=1800,
            _valid_from=time.time(),
        )
        fetch = mock.Mock(return_value=context_info)
        request._get_context_web_information = fetch  # type: ignore[method-assign]

        requests_with_header = []

        def _ensure():
            req = RequestOptions("https://contoso.sharepoint.com")
            request.ensure_form_digest(req)
            requests_with_header.append(req)

        _run_concurrently(_ensure)

        fetch.assert_called_once()
        self.assertTrue(all(req.headers.get("X-RequestDigest") == "digest" for req in requests_with_header))

    def test_split_batches_preserves_order_and_drains_queue(self):
        ctx = ClientContext("https://contoso.sharepoint.com")
        for _ in range(250):
            ctx.add_query(ClientQuery(ctx))

        batches = ctx._split_batches(100)

        self.assertEqual([len(batch.queries) for batch in batches], [100, 100, 50])
        self.assertFalse(ctx.has_pending_request)
        self.assertIsNone(ctx._current_query)

    def test_clone_shares_auth_and_transport(self):
        ctx = ClientContext("https://contoso.sharepoint.com")
        ctx.add_query(ClientQuery(ctx))
        source_request = ctx.pending_request()

        clone = ctx.clone("https://contoso-admin.sharepoint.com")

        clone_request = clone.pending_request()
        self.assertIs(clone_request.authentication_context, source_request.authentication_context)
        self.assertIs(clone_request.transport, source_request.transport)
        self.assertFalse(clone.has_pending_request)
        self.assertTrue(ctx.has_pending_request)

    def test_clone_keeps_pending_queries(self):
        ctx = ClientContext("https://contoso.sharepoint.com")
        for _ in range(3):
            ctx.add_query(ClientQuery(ctx))

        clone = ctx.clone("https://contoso-admin.sharepoint.com", clear_queries=False)

        self.assertEqual(len(clone._queries), 3)
        self.assertTrue(clone.has_pending_request)


if __name__ == "__main__":
    unittest.main()
