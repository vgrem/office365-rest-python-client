"""Offline tests for the ``Entity.update_properties`` write helper.

``update_properties(**values)`` is sugar over repeated ``set_property`` calls
plus a single queued ``update()``: it coerces values the same way, stays
deferred until ``execute_query()`` and works for both the Graph and SharePoint
entity bases.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.http.http_method import HttpMethod
from office365.sharepoint.client_context import ClientContext
from tests import test_site_url
from tests._scripted_transport import ScriptedTransport


class _RecordingTransport(ScriptedTransport):
    """Scripted transport that also records the requests it received."""

    def __init__(self, payloads):
        super().__init__(payloads)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        return super().execute(request)


def _graph(payloads):
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    transport = _RecordingTransport(payloads)
    client.pending_request().transport = transport
    return client, transport


def _sp(payloads):
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    transport = _RecordingTransport(payloads)
    ctx.pending_request().transport = transport
    return ctx, transport


# --- deferred, single request -------------------------------------------------


def test_graph_update_properties_is_deferred_and_returns_self():
    client, transport = _graph([])
    user = client.users["jdoe@contoso.com"]

    returned = user.update_properties(displayName="John Doe", jobTitle="Engineer")

    assert transport.calls == 0
    assert returned is user
    assert len(client._queries) == 1
    # values are readable through the typed accessors, exactly like set_property
    assert user.display_name == "John Doe"


def test_graph_update_properties_sends_single_patch():
    client, transport = _graph([{"id": "1"}])
    user = client.users["jdoe@contoso.com"]

    user.update_properties(displayName="John Doe", jobTitle="Engineer").execute_query()

    assert transport.calls == 1
    request = transport.requests[0]
    assert request.method == HttpMethod.Patch
    assert request.data["displayName"] == "John Doe"
    assert request.data["jobTitle"] == "Engineer"


def test_sharepoint_update_properties_is_deferred():
    ctx, transport = _sp([])
    web = ctx.web

    web.update_properties(Title="Contoso")

    assert transport.calls == 0
    assert len(ctx._queries) == 1
    assert web.title == "Contoso"


def test_sharepoint_update_properties_sends_single_merge():
    ctx, transport = _sp([{"d": {}}])

    ctx.web.update_properties(Title="Contoso", Description="Team site").execute_query()

    assert transport.calls == 1
    request = transport.requests[0]
    assert request.method == HttpMethod.Post
    assert request.headers.get("X-HTTP-Method") == "MERGE"
    assert request.url.endswith("/Web")
    assert request.data["Title"] == "Contoso"
    assert request.data["Description"] == "Team site"
