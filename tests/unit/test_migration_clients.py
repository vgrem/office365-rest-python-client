"""`migration_client` decides the workload policy; a client only carries it.

Three decisions live in that one function and nowhere else: a Graph context is sent with the
priority header while a SharePoint context is not (SharePoint signals load with its health
score, not with this header), ``priority=None`` leaves the header off, and pacing is installed
unless the caller declines it. The header's own mechanics — the name, the rejected value — are
covered by ``test_runtime_retry.py``, so they are not restated here.

A tenant run cannot show any of this: what it shows is that an export completed, which is also
what it shows when the header is missing.
"""

from __future__ import annotations

from typing import Optional

from office365.graph_client import GraphClient
from office365.migration import migration_client
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext

PRIORITY_HEADER = "x-ms-throttle-priority"


def _header(client: ClientRuntimeContext) -> Optional[str]:
    """Read one header off the request this client would send, without sending it."""
    request = RequestOptions(url="https://contoso.example/v1.0/me")
    client.pending_request().beforeExecute(request)
    return request.headers.get(PRIORITY_HEADER)


def _unauthenticated(client: ClientRuntimeContext) -> ClientRuntimeContext:
    """Drop the hooks that would authenticate a request that is never sent."""
    client.pending_request().beforeExecute.clear()
    return client


def test_a_graph_client_is_sent_as_background_work():
    assert _header(migration_client(_unauthenticated(GraphClient()))) == "low"


def test_the_priority_reaches_the_request():
    client = migration_client(_unauthenticated(GraphClient()), priority="high")

    assert _header(client) == "high"


def test_the_header_can_be_left_off():
    client = migration_client(_unauthenticated(GraphClient()), priority=None)

    assert _header(client) is None


def test_a_sharepoint_context_is_paced_but_carries_no_graph_header():
    ctx = migration_client(_unauthenticated(ClientContext("https://contoso.sharepoint.com")))

    assert ctx.rate_limiter is not None
    assert _header(ctx) is None


def test_pacing_is_installed_unless_declined():
    assert migration_client(_unauthenticated(GraphClient())).rate_limiter is not None
    assert migration_client(_unauthenticated(GraphClient()), pace=False).rate_limiter is None


def test_the_client_is_returned_for_chaining():
    client = _unauthenticated(GraphClient())

    assert migration_client(client) is client
