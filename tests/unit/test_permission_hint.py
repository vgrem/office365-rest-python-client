"""A denied request names the grant the called API declares.

``@require_permission`` tags the query it built, so a 403 can say *what* was
missing instead of only that something was. It must not say it on an unrelated
failure, nor on a call that declares nothing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from office365.graph_client import GraphClient
from office365.migration.offline import offline_sharepoint_context
from office365.runtime.exceptions import AccessDeniedException
from office365.sharepoint.client_context import ClientContext
from tests._scripted_transport import ScriptedTransport

_DENIED = ("deny",)
_SERVER_ERROR = {
    "http_status": 500,
    "body": {"error": {"code": "InternalServerError", "message": "The server is unwell."}},
}


def _graph(payloads) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = ScriptedTransport(payloads)
    return client


def _sharepoint(payloads) -> ClientContext:
    context = offline_sharepoint_context()
    context.pending_request().beforeExecute.clear()
    context.pending_request().transport = ScriptedTransport(payloads)
    return context


def _subscribe(client: GraphClient):
    return client.subscriptions.add(
        change_type="updated",
        notification_url="https://contoso.com/notify",
        resource="users",
        expiration=datetime.now(timezone.utc) + timedelta(hours=1),
    )


def test_a_denied_declared_call_names_the_scope_it_needs():
    with pytest.raises(AccessDeniedException) as denied:
        _subscribe(_graph([_DENIED])).execute_query()

    (hint,) = denied.value.hints
    assert "Subscription.Read.All" in hint
    assert hint in str(denied.value)


def test_a_denied_call_on_another_api_names_that_api():
    context = _sharepoint([_DENIED])

    with pytest.raises(AccessDeniedException) as denied:
        context.site.get_migration_status().execute_query()

    (hint,) = denied.value.hints
    assert "SharePoint" in hint


def test_a_failure_that_is_not_a_denial_carries_no_hint():
    with pytest.raises(Exception) as failed:
        _subscribe(_graph([_SERVER_ERROR])).execute_query()

    assert getattr(failed.value, "hints", ()) == ()


def test_a_denied_call_that_declares_nothing_says_nothing():
    """``Entity.get`` declares no permission, so it has none to name."""
    with pytest.raises(AccessDeniedException) as denied:
        _graph([_DENIED]).me.get().execute_query()

    assert denied.value.hints == ()
