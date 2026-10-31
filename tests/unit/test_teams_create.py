"""Offline tests for the creation payloads ``TeamCollection`` and ``ChannelCollection`` build.

Application-context team creation must name at least one owner, so
``create``/``create_and_wait`` accept an ``owners`` argument that is rendered as
``aadUserConversationMember`` entries in the request body.

A channel created asynchronously (HTTP 202) is covered here too.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.paths.resource_path import ResourcePath
from office365.teams.channels.collection import ChannelCollection
from tests._scripted_transport import ScriptedTransport

_OPERATION = {
    "http_status": 202,
    "headers": {"Location": "https://graph.microsoft.com/v1.0/teams/abc/operations/op1"},
    "body": {},
}


class _RecordingTransport(ScriptedTransport):
    """Scripted transport that also records the requests it received."""

    def __init__(self, payloads):
        super().__init__(payloads)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        return super().execute(request)


def _client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def test_create_with_owners_adds_conversation_members():
    transport = _RecordingTransport([_OPERATION])
    client = _client(transport)

    client.teams.create("Team A", "desc", "standard", owners=["ada@contoso.com"]).execute_query()

    assert transport.requests[-1].data["members"] == [
        {
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "roles": ["owner"],
            "user@odata.bind": "https://graph.microsoft.com/v1.0/users('ada@contoso.com')",
        }
    ]


_CREATED = {
    "http_status": 202,
    "headers": {
        "Content-Location": "https://graph.microsoft.com/v1.0/teams('abc')",
        "Location": "https://graph.microsoft.com/v1.0/teams/abc/operations/op1",
    },
    "body": {},
}
_OPERATION_SUCCEEDED = {"http_status": 200, "body": {"status": "succeeded", "targetResourceId": "abc"}}
_TEAM = {"http_status": 200, "body": {"id": "abc", "displayName": "Team A"}}


def test_create_and_wait_polls_inside_the_after_execute_hook():
    """The poll blocks inside the hook, then the queued reload runs on the outer loop.

    ``create_and_wait`` is one ``execute_query()``: submit, poll the operation, then
    reload the created team. The poll is a blocking wait, so it must not disturb the
    queue the outer loop is draining — the reload it queues is executed afterwards.
    """
    transport = _RecordingTransport([_CREATED, _OPERATION_SUCCEEDED, _TEAM])
    client = _client(transport)

    team = client.teams.create_and_wait("Team A").execute_query()

    assert team.id == "abc"
    assert team.display_name == "Team A"
    assert transport.calls == 3  # noqa: PLR2004 - create, poll, reload
    assert transport.requests[1].url.endswith("/teams/abc/operations/op1")


# --- Channel creation: an async (HTTP 202) add follows its operation ----------

_CHANNEL_ID = "19:abc@thread.tacv2"
_ACCEPTED = {
    "http_status": 202,
    "headers": {"Location": "/teams/t1/operations/op1"},
    "body": {},
}
_OPERATION_SUCCEEDED = {
    "http_status": 200,
    "headers": {"Content-Type": "application/json"},
    "body": {
        "status": "succeeded",
        # targetResourceId is the *team* id, not the channel id.
        "targetResourceId": "t1",
        "targetResourceLocation": f"/teams('t1')/channels('{_CHANNEL_ID}')",
    },
}
_CHANNEL = {
    "http_status": 200,
    "headers": {"Content-Type": "application/json"},
    "body": {"id": _CHANNEL_ID, "displayName": "Verify", "membershipType": "shared"},
}


def _channels(client: GraphClient) -> ChannelCollection:
    team_path = ResourcePath("t1", ResourcePath("teams"))
    return ChannelCollection(client, ResourcePath("channels", team_path))


def test_add_async_channel_follows_operation():
    transport = _RecordingTransport([_ACCEPTED, _OPERATION_SUCCEEDED, _CHANNEL])
    client = _client(transport)

    channel = _channels(client).add("Verify", membership_type="shared").execute_query()

    assert transport.calls == 3  # noqa: PLR2004
    assert channel.id == _CHANNEL_ID
    assert channel.display_name == "Verify"
