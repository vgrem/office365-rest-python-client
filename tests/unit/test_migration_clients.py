"""The migration workload policy, applied in one call."""

from __future__ import annotations

from typing import Optional

import pytest
from office365.graph_client import GraphClient
from office365.migration import migration_client
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext

PRIORITY_HEADER = "x-ms-throttle-priority"


def _header(client: ClientRuntimeContext, name: str) -> Optional[str]:
    """Run the client's pre-request hooks and read one header off the request."""
    request = RequestOptions(url="https://contoso.example/v1.0/me")
    client.pending_request().beforeExecute(request)
    return request.headers.get(name)


def _unauthenticated(client):
    """Drop the hooks that would authenticate a request we never send."""
    client.pending_request().beforeExecute.clear()
    return client


def test_graph_client_sends_low_priority():
    client = migration_client(_unauthenticated(GraphClient()))
    assert _header(client, PRIORITY_HEADER) == "low"


@pytest.mark.parametrize("priority", ["normal", "high"])
def test_priority_is_forwarded(priority):
    client = migration_client(_unauthenticated(GraphClient()), priority=priority)
    assert _header(client, PRIORITY_HEADER) == priority


def test_priority_can_be_left_off():
    client = migration_client(_unauthenticated(GraphClient()), priority=None)
    assert _header(client, PRIORITY_HEADER) is None


def test_pacing_is_installed_by_default():
    assert migration_client(_unauthenticated(GraphClient())).rate_limiter is not None


def test_pacing_can_be_left_off():
    assert migration_client(_unauthenticated(GraphClient()), pace=False).rate_limiter is None


def test_sharepoint_context_is_paced_but_carries_no_graph_header():
    """SharePoint paces on its health score; the priority header is Graph-only."""
    ctx = migration_client(_unauthenticated(ClientContext("https://contoso.sharepoint.com")))
    assert ctx.rate_limiter is not None
    assert _header(ctx, PRIORITY_HEADER) is None


def test_the_configured_client_is_returned_for_chaining():
    client = _unauthenticated(GraphClient())
    assert migration_client(client) is client
