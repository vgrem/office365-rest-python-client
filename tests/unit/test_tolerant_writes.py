"""Offline tests for the tolerant write helpers.

``ignore_missing=True`` makes ``delete_object`` / ``recycle`` idempotent: an
HTTP 404 is treated as success, while every other failure still propagates.
``ViewCollection.ensure_view`` is a deferred get-or-create.
"""

from __future__ import annotations

import pytest
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.exceptions import ObjectNotFoundException
from office365.sharepoint.views.view import View
from tests._scripted_transport import graph, sharepoint

_NOT_FOUND = {
    "http_status": 404,
    "body": {"error": {"code": "Request_ResourceNotFound", "message": "Resource not found"}},
}

_FORBIDDEN = {
    "http_status": 403,
    "body": {"error": {"code": "Forbidden", "message": "Access is denied."}},
}


# --- delete_object(ignore_missing=...) ---------------------------------------


def test_graph_delete_object_raises_when_missing_by_default():
    client, transport = graph([_NOT_FOUND], record=True)

    with pytest.raises(ObjectNotFoundException):
        client.users["missing@contoso.com"].delete_object().execute_query()

    assert transport.calls == 1


def test_graph_delete_object_propagates_non_404_even_with_ignore_missing():
    client, _ = graph([_FORBIDDEN], record=True)

    with pytest.raises(ClientRequestException):
        client.users["x@contoso.com"].delete_object(ignore_missing=True).execute_query()


# --- ViewCollection.ensure_view ----------------------------------------------


def _views(ctx):
    return ctx.web.lists.get_by_title("Documents").views


def test_ensure_view_creates_when_missing():
    ctx, transport = sharepoint([_NOT_FOUND, {"d": {"Id": "v1", "Title": "Active"}}], record=True)

    view = _views(ctx).ensure_view("Active", fields=["Title"]).execute_query()

    assert transport.calls == 2  # noqa: PLR2004
    assert isinstance(view, View)
    assert view.title == "Active"
    assert view.id == "v1"
    # the second request is the Add; the created view stays addressable by title
    assert "GetByTitle" in str(view.resource_path)


def test_ensure_view_on_conflict_update_reconciles_scalar_settings():
    ctx, transport = sharepoint(
        [
            {"d": {"Id": "v1", "Title": "Active", "RowLimit": 30}},
            {},
        ],
        record=True,
    )

    view = _views(ctx).ensure_view("Active", row_limit=50, on_conflict="update").execute_query()

    assert transport.calls == 2  # noqa: PLR2004
    assert view.row_limit == 50  # noqa: PLR2004
