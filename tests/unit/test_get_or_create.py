"""Tests for the shared idempotent get-or-create primitives.

``ClientObject.get_or_none`` is the read-side twin: it only queues a read, and
swallows the 404 the way the create half tolerates a miss.
"""

from __future__ import annotations

import pytest
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.queries.get_or_create import get_or_create
from tests._scripted_transport import ScriptedTransport


class _FakeContext:
    def __init__(self) -> None:
        self._queries: list[object] = []

    def add_query(self, query):
        self._queries.append(query)
        return self


class _FakeEntity:
    def __init__(self, context: _FakeContext) -> None:
        self.context = context
        self._after: list = []
        self._error: list = []
        self.copied_from = None
        self.updated = False

    def after_execute(self, action, execute_first=False):
        self._after.append(action)
        return self

    def on_error(self, action):
        self._error.append(action)
        return self

    def copy_from(self, other):
        self.copied_from = other

    def update(self):
        self.updated = True


def test_get_or_create_returns_existing_when_found():
    ctx = _FakeContext()
    return_type = _FakeEntity(ctx)
    found = _FakeEntity(ctx)

    result = get_or_create(find=lambda: found, create_query=object, return_type=return_type)

    assert result is return_type
    found._after[0](found)
    assert return_type.copied_from is found
    assert ctx._queries == []  # the placeholder resolved (no create)


def test_get_or_create_tolerant_miss_defers_create():
    ctx = _FakeContext()
    return_type = _FakeEntity(ctx)
    found = _FakeEntity(ctx)
    create_query = object()

    get_or_create(
        find=lambda: found,
        create_query=lambda: create_query,
        return_type=return_type,
        missing=lambda entity: True,
    )
    barrier = ctx._queries[-1]
    found._after[0](found)

    assert create_query in ctx._queries
    assert barrier not in ctx._queries
    assert return_type.copied_from is None


# --- ClientObject.get_or_none: the read-side twin -----------------------------

_NOT_FOUND = {
    "http_status": 404,
    "body": {"error": {"code": "Request_ResourceNotFound", "message": "Resource not found"}},
}

_FORBIDDEN = {
    "http_status": 403,
    "body": {"error": {"code": "Forbidden", "message": "Access is denied."}},
}


def _client(payloads):
    transport = ScriptedTransport(payloads)
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def test_get_or_none_defers_until_execute():
    client, transport = _client([{"id": "t1", "displayName": "Team One"}])

    team = client.teams["t1"].get_or_none()

    # a deferred builder must not hit the wire on its own
    assert transport.calls == 0
    assert not team.is_loaded

    team.execute_query()

    assert transport.calls == 1
    assert team.is_loaded
    assert team.get_property("id") == "t1"


def test_get_or_none_propagates_non_404_errors():
    client, _ = _client([_FORBIDDEN])

    team = client.teams["t1"].get_or_none()

    with pytest.raises(ClientRequestException):
        team.execute_query()

    assert not team.is_loaded
