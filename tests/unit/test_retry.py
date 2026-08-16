from __future__ import annotations

import unittest
from unittest import mock

import requests
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from requests import Response


def _make_error_response(status_code: int, headers: dict | None = None) -> Response:
    resp = Response()
    resp.status_code = status_code
    resp.url = "https://contoso.sharepoint.com/_api/web"
    resp.headers.update(headers or {})
    resp._content = b'{"error":{"code":"-1, System.Exception","message":"boom"}}'
    return resp


def _make_exception(status_code: int, headers: dict | None = None) -> ClientRequestException:
    return ClientRequestException.from_response(_make_error_response(status_code, headers))


def _make_context(outcomes: list[Exception | None]) -> tuple[ClientContext, mock.Mock]:
    """ClientContext whose execute_query replays the scripted outcomes.

    ``None`` signals a successful execution; an exception is raised as-is.
    Attempts are read from ``execute_query.call_count``.
    """
    ctx = ClientContext("https://contoso.sharepoint.com")
    execute_query = mock.Mock(side_effect=outcomes)
    ctx.execute_query = execute_query  # type: ignore[method-assign]
    return ctx, execute_query


class TestExecuteQueryRetry(unittest.TestCase):
    def test_permanent_error_raises_immediately(self):
        ctx, execute_query = _make_context([_make_exception(400)])

        with mock.patch("office365.runtime.client_runtime_context.sleep") as sleep_mock:
            with self.assertRaises(ClientRequestException):
                ctx.execute_query_retry(max_retry=5, timeout_secs=5)

        self.assertEqual(execute_query.call_count, 1)
        sleep_mock.assert_not_called()

    def test_transient_then_success(self):
        ctx, execute_query = _make_context([_make_exception(429), None])

        with mock.patch("office365.runtime.client_runtime_context.sleep") as sleep_mock:
            ctx.execute_query_retry(max_retry=5, timeout_secs=5)

        self.assertEqual(execute_query.call_count, 2)
        sleep_mock.assert_called_once_with(5)

    def test_retries_exhausted_raises_last_error(self):
        ctx, execute_query = _make_context([_make_exception(503), _make_exception(503), _make_exception(503)])

        with self.assertRaises(ClientRequestException) as cm:
            ctx.execute_query_retry(max_retry=2, timeout_secs=1)

        self.assertEqual(execute_query.call_count, 2)
        assert cm.exception.response is not None
        self.assertEqual(cm.exception.response.status_code, 503)

    def test_non_http_error_is_retried(self):
        ctx, execute_query = _make_context([requests.ConnectionError("boom"), None])

        ctx.execute_query_retry(
            max_retry=5,
            timeout_secs=1,
            exceptions=(ClientRequestException, requests.RequestException),
        )

        self.assertEqual(execute_query.call_count, 2)

    def test_incremental_retry_does_not_retry_permanent_error(self):
        ctx, execute_query = _make_context([_make_exception(400)])

        with self.assertRaises(ClientRequestException):
            ctx.execute_query_with_incremental_retry(max_retry=5)

        self.assertEqual(execute_query.call_count, 1)

    def test_incremental_retry_applies_retry_after(self):
        ctx, execute_query = _make_context([_make_exception(429, {"Retry-After": "10"}), None])

        with mock.patch("office365.runtime.client_runtime_context.sleep") as sleep_mock:
            ctx.execute_query_with_incremental_retry(max_retry=5)

        self.assertEqual(execute_query.call_count, 2)
        sleep_mock.assert_called_once_with(10)

    def test_incremental_retry_falls_back_to_default_timeout(self):
        ctx, execute_query = _make_context([_make_exception(503), None])

        with mock.patch("office365.runtime.client_runtime_context.sleep") as sleep_mock:
            ctx.execute_query_with_incremental_retry(max_retry=5)

        self.assertEqual(execute_query.call_count, 2)
        sleep_mock.assert_called_once_with(5)
