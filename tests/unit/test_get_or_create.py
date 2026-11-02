"""Tests for the shared idempotent get-or-create primitives.

``ClientObject.get_or_none`` is the read-side twin: it only queues a read, and
swallows the 404 the way the create half tolerates a miss.
"""

from __future__ import annotations

import pytest
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.http_method import HttpMethod
from tests._scripted_transport import RecordingTransport

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
    transport = RecordingTransport(payloads)
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def test_ensure_returns_existing_domain_without_creating():
    client, transport = _client([{"id": "contoso.com", "isVerified": True}])

    domain = client.domains.ensure("contoso.com")
    assert transport.calls == 0
    domain.execute_query()

    assert [request.method for request in transport.requests] == [HttpMethod.Get]
    assert domain.id == "contoso.com"
    assert domain.get_property("isVerified") is True


def test_ensure_creates_missing_domain_before_dependent_read():
    client, transport = _client([_NOT_FOUND, {"id": "contoso.com"}, {"id": "contoso.com", "isVerified": False}])

    domain = client.domains.ensure("contoso.com")
    domain.get()
    assert transport.calls == 0
    domain.execute_query()

    assert [request.method for request in transport.requests] == [HttpMethod.Get, HttpMethod.Post, HttpMethod.Get]
    assert transport.requests[1].url.endswith("/domains")
    assert transport.requests[2].url.endswith("/domains/contoso.com")
    assert domain.id == "contoso.com"


def test_ensure_propagates_forbidden_without_creating():
    client, transport = _client([_FORBIDDEN])

    domain = client.domains.ensure("contoso.com")
    with pytest.raises(ClientRequestException):
        domain.execute_query()

    assert [request.method for request in transport.requests] == [HttpMethod.Get]


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
