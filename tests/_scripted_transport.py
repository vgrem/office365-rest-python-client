"""Shared scripted HTTP transport for offline unit tests (no network).

Payload forms handled by :class:`ScriptedTransport`:

- a plain dict (e.g. ``{"d": {...}}``) -> ``200`` verbose JSON
- ``("deny",)`` -> ``403`` access-denied JSON
- ``{"status": int, "retry_after": int, "health_score": int, "body": dict}``
  -> status + throttling headers + body
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


class ScriptedTransport(BaseTransport):
    """Returns one scripted response per call, in order."""

    def __init__(self, payloads: list[Any]) -> None:
        self._payloads = payloads
        self.calls = 0

    def execute(self, request):
        payload = self._payloads[self.calls]
        self.calls += 1
        resp = Response()
        resp.url = request.url

        if isinstance(payload, tuple) and payload[0] == "deny":
            resp.status_code = 403
            resp.headers.update({"Content-Type": "application/json"})
            resp._content = _json.dumps(_DENIED).encode("utf-8")
        elif isinstance(payload, dict) and "status" in payload:
            resp.status_code = int(payload["status"])
            resp.headers.update({"Content-Type": "application/json"})
            if "retry_after" in payload:
                resp.headers["Retry-After"] = str(payload["retry_after"])
            if "health_score" in payload:
                resp.headers["X-SharePointHealthScore"] = str(payload["health_score"])
            resp._content = _json.dumps(payload.get("body", {"d": {"results": []}})).encode("utf-8")
        else:
            resp.status_code = 200
            resp.headers.update({"Content-Type": "application/json;odata=verbose"})
            resp._content = _json.dumps(payload).encode("utf-8")
        return resp
