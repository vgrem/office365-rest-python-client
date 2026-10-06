"""Offline tests for ``ClientObjectCollection.first`` / ``single``.

``single`` must bound its query to ``$top=2`` so an ambiguous match is rejected
without downloading every matching item, while ``first`` stays at ``$top=1``.
"""

from __future__ import annotations

import pytest
from office365.graph_client import GraphClient
from office365.runtime.types.exceptions import NotFoundException
from tests._scripted_transport import ScriptedTransport

GROUP = {"id": "g1", "displayName": "Group One"}


class _RecordingTransport(ScriptedTransport):
    """Scripted transport that also records the request URLs it received."""

    def __init__(self, payloads):
        super().__init__(payloads)
        self.urls: list[str] = []

    def execute(self, request):
        self.urls.append(request.url)
        return super().execute(request)


def _client(payloads):
    transport = _RecordingTransport(payloads)
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def test_single_bounds_query_with_top_2():
    client, transport = _client([{"value": [GROUP]}])

    client.groups.single("displayName eq 'Group One'")
    client.execute_query()

    assert len(transport.urls) == 1
    assert "$top=2" in transport.urls[0]


def test_single_returns_the_match():
    client, _ = _client([{"value": [GROUP]}])

    group = client.groups.single("displayName eq 'Group One'")
    client.execute_query()

    assert group.get_property("id") == "g1"
    assert group.get_property("displayName") == "Group One"


def test_single_raises_when_no_match():
    client, _ = _client([{"value": []}])

    client.groups.single("displayName eq 'Missing'")

    with pytest.raises(NotFoundException):
        client.execute_query()


def test_single_raises_when_ambiguous():
    client, _ = _client([{"value": [GROUP, {"id": "g2", "displayName": "Group One"}]}])

    client.groups.single("displayName eq 'Group One'")

    with pytest.raises(ValueError):
        client.execute_query()


def test_first_bounds_query_with_top_1():
    client, transport = _client([{"value": [GROUP]}])

    client.groups.first("displayName eq 'Group One'")
    client.execute_query()

    assert len(transport.urls) == 1
    assert "$top=1" in transport.urls[0]
