"""Offline tests for the unified single-entity ``upsert`` verb.

``RecordCollection.upsert`` reconciles client-side: a tolerant ``$filter``
lookup, then a create when missing or a write-idempotent update when present.
The create runs in the lookup's queue slot (via a barrier), so anything queued
after the upsert still runs after the resource exists.
"""

from __future__ import annotations

import pytest
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.odata.literals import odata_literal
from tests._scripted_transport import graph, sharepoint

_EXISTING = {"id": "g1", "displayName": "Group157", "description": "Old"}
_CREATED = {"id": "g1", "displayName": "Group157", "description": "Team site"}


def _methods(transport):
    return [request.method for request in transport.requests]


# ── odata_literal ────────────────────────────────────────────────


def test_odata_literal_emits_numbers_booleans_and_null_bare():
    assert odata_literal(42) == "42"
    assert odata_literal(True) == "true"
    assert odata_literal(False) == "false"
    assert odata_literal(None) == "null"


# ── upsert: create when missing ──────────────────────────────────


def test_upsert_creates_when_missing():
    client, transport = graph([{"value": []}, _CREATED], record=True)

    group = client.groups.upsert("uniqueName", "Group157", displayName="Group157", description="Team site")
    assert transport.calls == 0
    group.execute_query()

    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Post]
    assert "uniqueName eq 'Group157'" in transport.requests[0].url
    assert transport.requests[1].url.endswith("/groups")
    assert transport.requests[1].data == {
        "uniqueName": "Group157",
        "displayName": "Group157",
        "description": "Team site",
    }
    assert group.id == "g1"
    assert group.display_name == "Group157"


def test_upsert_creates_with_only_the_key_when_no_properties():
    client, transport = graph([{"value": []}, {"id": "g1", "uniqueName": "Group157"}], record=True)

    group = client.groups.upsert("uniqueName", "Group157").execute_query()

    assert transport.requests[1].data == {"uniqueName": "Group157"}
    assert group.is_loaded


# ── upsert: reconcile when present ───────────────────────────────


def test_upsert_updates_changed_properties():
    client, transport = graph([{"value": [_EXISTING]}, _EXISTING], record=True)

    group = client.groups.upsert("uniqueName", "Group157", description="New").execute_query()

    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Patch]
    assert transport.requests[1].url.endswith("/groups/g1")
    assert transport.requests[1].data["description"] == "New"
    assert group.id == "g1"


def test_upsert_is_write_idempotent_when_state_matches():
    client, transport = graph([{"value": [_EXISTING]}], record=True)

    group = client.groups.upsert("uniqueName", "Group157", description="Old")
    assert transport.calls == 0
    group.execute_query()

    assert _methods(transport) == [HttpMethod.Get]
    assert group.id == "g1"
    assert group.description == "Old"


def test_upsert_propagates_forbidden_lookup_without_creating():
    client, transport = graph(
        [{"http_status": 403, "body": {"error": {"code": "Forbidden", "message": "Access is denied."}}}], record=True
    )

    group = client.groups.upsert("uniqueName", "Group157")
    with pytest.raises(ClientRequestException):
        group.execute_query()

    assert _methods(transport) == [HttpMethod.Get]


# ── upsert: identity formatting ──────────────────────────────────


# ── upsert: deferred ordering ────────────────────────────────────


def test_upsert_create_runs_before_queries_queued_after_it():
    client, transport = graph([{"value": []}, _CREATED, _CREATED], record=True)

    group = client.groups.upsert("uniqueName", "Group157", description="Team site")
    group.get()  # dependent read queued after the upsert
    group.execute_query()

    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Post, HttpMethod.Get]
    assert transport.requests[1].url.endswith("/groups")
    assert transport.requests[2].url.endswith("/groups/g1")


# ── upsert: SharePoint parity ────────────────────────────────────


def test_upsert_creates_list_when_missing():
    ctx, transport = sharepoint([{"d": {"results": []}}, {"d": {"Id": "list-1", "Title": "Documents"}}], record=True)

    result = ctx.web.lists.upsert("Title", "Documents").execute_query()

    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Post]
    assert "Title eq 'Documents'" in transport.requests[0].url
    assert transport.requests[1].data == {"Title": "Documents"}
    assert result.get_property("Id") == "list-1"


def test_upsert_updates_existing_list():
    ctx, transport = sharepoint(
        [{"d": {"results": [{"Id": "list-1", "Title": "Documents", "Description": "Old"}]}}, {}], record=True
    )

    result = ctx.web.lists.upsert("Title", "Documents", Description="New").execute_query()

    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Post]
    assert transport.requests[1].headers["X-HTTP-Method"] == "MERGE"
    assert "Description" in transport.requests[1].data
    assert result.get_property("Description") == "New"
