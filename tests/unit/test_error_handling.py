"""What a failure says, and what it does not.

``ClientRequest`` hands an error to whichever handler is registered and then re-raises it, so
a handler must not swallow the failures that follow. And a refused call names the grant the
*called API* declares - the hint ``@require_permission`` attaches to the query - while an
unrelated failure, and a call that declares nothing, say nothing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from office365.graph_client import GraphClient
from office365.runtime.exceptions import AccessDeniedException, ObjectNotFoundException
from tests._scripted_transport import graph, sharepoint

_NOT_FOUND = {
    "http_status": 404,
    "body": {"error": {"code": "Request_ResourceNotFound", "message": "Resource not found"}},
}

_OK = {"d": {"Title": "Site"}}

_DENIED = ("deny",)

_SERVER_ERROR = {
    "http_status": 500,
    "body": {"error": {"code": "InternalServerError", "message": "The server is unwell."}},
}


def test_scoped_handler_left_by_finished_query_does_not_swallow_later_failure():
    # q1 succeeds; the handler registered for it stays on the request. q2 then
    # fails and must propagate because that stale handler no longer matches.
    ctx = sharepoint([_OK, _NOT_FOUND])[0]
    ctx.web.get()
    ctx.on_error(lambda _e: None)  # scoped to q1
    ctx.web.get()  # q2

    with pytest.raises(ObjectNotFoundException):
        ctx.execute_query()


def test_handler_once_is_removed_after_match():
    ctx = sharepoint([_NOT_FOUND, _NOT_FOUND])[0]
    handled = []
    ctx.pending_request().on_error(handled.append, once=True, condition=lambda: True)

    ctx.web.get().execute_query()
    with pytest.raises(ObjectNotFoundException):
        ctx.web.get().execute_query()

    assert len(handled) == 1


def _subscribe(client: GraphClient):
    return client.subscriptions.add(
        change_type="updated",
        notification_url="https://contoso.com/notify",
        resource="users",
        expiration=datetime.now(timezone.utc) + timedelta(hours=1),
    )


def test_a_denied_declared_call_names_the_scope_it_needs():
    with pytest.raises(AccessDeniedException) as denied:
        _subscribe(graph([_DENIED])[0]).execute_query()

    (hint,) = denied.value.hints
    assert "Subscription.Read.All" in hint
    assert hint in str(denied.value)


def test_a_denied_call_on_another_api_names_that_api():
    context = sharepoint([_DENIED])[0]

    with pytest.raises(AccessDeniedException) as denied:
        context.site.get_migration_status().execute_query()

    (hint,) = denied.value.hints
    assert "SharePoint" in hint


def test_a_failure_that_is_not_a_denial_carries_no_hint():
    with pytest.raises(Exception) as failed:
        _subscribe(graph([_SERVER_ERROR])[0]).execute_query()

    assert getattr(failed.value, "hints", ()) == ()


def test_a_denied_call_that_declares_nothing_says_nothing():
    """``Entity.get`` declares no permission, so it has none to name."""
    with pytest.raises(AccessDeniedException) as denied:
        graph([_DENIED])[0].me.get().execute_query()

    assert denied.value.hints == ()
