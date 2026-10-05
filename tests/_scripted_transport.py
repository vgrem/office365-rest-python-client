"""Shared scripted HTTP transports for offline unit tests (no network).

Payload forms handled by both transports:

- plain ``bytes``/``bytearray`` -> ``200`` with ``application/octet-stream`` body
- a plain dict (e.g. ``{"d": {...}}``) -> ``200`` verbose JSON
- ``("deny",)`` -> ``403`` access-denied JSON
- ``{"status": int, "retry_after": int, "health_score": int, "body": dict|bytes}``
  -> status + throttling headers + body (``bytes`` bodies are octet-stream,
  which lets a test script a ``206`` partial-content range response)
- ``{"http_status": int, "headers": dict, "body": dict|bytes}`` -> an arbitrary
  status + custom headers + JSON/octet-stream body, used to script 202
  long-running-operation poll responses (``headers`` carries
  ``Location``/``Operation-Location``/``Retry-After``)

:class:`ScriptedTransport` returns payloads in call order;
:class:`RoutingTransport` picks the first route whose URL substring matches;
:class:`AsyncScriptedTransport` is the native-async twin that only implements
``execute_async``.
"""

from __future__ import annotations

import json as _json
from typing import Any

from office365.runtime.transport.base import BaseTransport
from requests import Response

_DENIED = {
    "error": {
        "code": "-2147024891, System.UnauthorizedAccessException",
        "message": {"value": "Access is denied."},
    }
}


def build_response(request, payload: Any) -> Response:
    """Build a :class:`requests.Response` for one scripted payload."""
    resp = Response()
    resp.url = request.url

    if isinstance(payload, (bytes, bytearray)):
        resp.status_code = 200
        resp.headers.update({"Content-Type": "application/octet-stream", "Content-Length": str(len(payload))})
        resp._content = bytes(payload)
    elif isinstance(payload, tuple) and payload[0] == "deny":
        resp.status_code = 403
        resp.headers.update({"Content-Type": "application/json"})
        resp._content = _json.dumps(_DENIED).encode("utf-8")
    elif isinstance(payload, dict) and "http_status" in payload:
        resp.status_code = int(payload["http_status"])
        resp.headers.update(payload.get("headers") or {})
        body = payload.get("body")
        if body is None:
            resp._content = b""
        elif isinstance(body, (bytes, bytearray)):
            resp.headers.setdefault("Content-Type", "application/octet-stream")
            resp._content = bytes(body)
        else:
            resp.headers.setdefault("Content-Type", "application/json")
            resp._content = _json.dumps(body).encode("utf-8")
    elif isinstance(payload, dict) and "status" in payload:
        resp.status_code = int(payload["status"])
        body = payload.get("body", {"d": {"results": []}})
        if isinstance(body, (bytes, bytearray)):
            resp.headers.update({"Content-Type": "application/octet-stream", "Content-Length": str(len(body))})
            resp._content = bytes(body)
        else:
            resp.headers.update({"Content-Type": "application/json"})
            resp._content = _json.dumps(body).encode("utf-8")
        if "retry_after" in payload:
            resp.headers["Retry-After"] = str(payload["retry_after"])
        if "health_score" in payload:
            resp.headers["X-SharePointHealthScore"] = str(payload["health_score"])
    else:
        resp.status_code = 200
        resp.headers.update({"Content-Type": "application/json;odata=verbose"})
        resp._content = _json.dumps(payload).encode("utf-8")
    # The body is materialised, so the response behaves like a fully-read one
    # (`iter_content` slices `_content` instead of reading a live `raw`).
    resp._content_consumed = True
    return resp


class ScriptedTransport(BaseTransport):
    """Returns one scripted response per call, in order."""

    def __init__(self, payloads: list[Any]) -> None:
        self._payloads = payloads
        self.calls = 0

    def execute(self, request):
        payload = self._payloads[self.calls]
        self.calls += 1
        return build_response(request, payload)


class RoutingTransport(BaseTransport):
    """Returns the payload of the first route whose key is a substring of the URL.

    Order-independent, so it is safe for concurrent requests.
    """

    def __init__(self, routes: list[tuple[str, Any]]) -> None:
        self._routes = routes
        self.calls: list[str] = []
        self.requests: list[Any] = []

    def execute(self, request):
        url = request.url
        self.calls.append(url)
        self.requests.append(request)
        for key, payload in self._routes:
            if key in url:
                return build_response(request, payload)
        raise AssertionError(f"RoutingTransport: no route matched {url}")


class AsyncScriptedTransport(BaseTransport):
    """Returns one scripted response per call, natively on the event loop.

    Only the asynchronous path is implemented. The synchronous :meth:`execute`
    raises, so a test that accidentally drives this transport from blocking code
    fails loudly instead of silently passing through a worker thread.
    """

    def __init__(self, payloads: list[Any]) -> None:
        self._payloads = payloads
        self.calls = 0

    def execute(self, request):
        raise NotImplementedError("AsyncScriptedTransport only supports execute_async")

    async def execute_async(self, request):
        payload = self._payloads[self.calls]
        self.calls += 1
        return build_response(request, payload)
