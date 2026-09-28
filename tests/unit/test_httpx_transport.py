"""Tests for the optional httpx-backed transport (skipped when httpx is absent)."""

from __future__ import annotations

import asyncio
import json

import pytest
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.httpx_transport import HttpxTransport
from office365.sharepoint.client_context import ClientContext

httpx = pytest.importorskip("httpx")

_URL = "https://graph.microsoft.com/v1.0/me"


def _json_handler(payload: dict):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    return handler


def _transport(handler) -> HttpxTransport:
    return HttpxTransport(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        async_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def test_execute_async_adapts_response() -> None:
    transport = _transport(_json_handler({"d": {"Title": "Contoso"}}))

    response = asyncio.run(transport.execute_async(RequestOptions(url=_URL)))

    assert response.status_code == 200  # noqa: PLR2004
    assert response.json() == {"d": {"Title": "Contoso"}}
    assert response.headers["Content-Type"].startswith("application/json")


def test_execute_sync_adapts_response() -> None:
    transport = _transport(_json_handler({"ok": True}))

    response = transport.execute(RequestOptions(url=_URL))

    assert response.status_code == 200  # noqa: PLR2004
    assert response.json() == {"ok": True}


def test_execute_async_sends_json_body() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["body"] = request.content
        return httpx.Response(200, json={"ok": True})

    transport = _transport(handler)
    request = RequestOptions(url=_URL, method=HttpMethod.Post, data={"Title": "x"})

    asyncio.run(transport.execute_async(request))

    assert seen["method"] == "POST"
    assert json.loads(seen["body"]) == {"Title": "x"}  # type: ignore[arg-type]


def test_streamed_body_iterates() -> None:
    body = b"0123456789" * 100

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body)

    transport = _transport(handler)

    response = asyncio.run(transport.execute_async(RequestOptions(url=_URL, stream=True)))

    chunks = list(response.iter_content(chunk_size=16))
    assert b"".join(chunks) == body


def test_aclose_closes_both_clients() -> None:
    transport = _transport(_json_handler({}))
    async_client = transport._async_client
    sync_client = transport._client

    asyncio.run(transport.aclose())

    assert async_client.is_closed
    assert sync_client.is_closed


def test_context_execute_query_async_uses_httpx_transport() -> None:
    ctx = ClientContext("https://contoso.sharepoint.com")
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().with_async_transport(_transport(_json_handler({"d": {"Title": "Contoso"}})))
    ctx.load(ctx.web)

    asyncio.run(ctx.execute_query_async())

    assert ctx.web.properties.get("Title") == "Contoso"
