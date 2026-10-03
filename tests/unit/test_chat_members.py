"""Tests for chat navigation paths after creation (offline)."""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.paths.resource_path import ResourcePath
from office365.teams.chats.collection import ChatCollection
from office365.teams.chats.type import ChatType


def test_chat_members_path_follows_id_after_create():
    """A chat created via ``ChatCollection.add`` must expose ``/chats/{id}/members``.

    ``ChatCollection.add`` populates the ``members`` navigation to build the POST
    body while the new chat still has no id. If that chat is not given a shared
    placeholder path, the navigation is cached against a parentless
    ``ResourcePath`` and keeps resolving to ``/members`` even after the create
    response assigns the id.
    """
    client = GraphClient(tenant="contoso.onmicrosoft.com")
    chats = ChatCollection(client, ResourcePath("chats"))

    chat = chats.add(ChatType.oneOnOne, owner_ids=["owner-1", "owner-2"])
    chat.set_property("id", "19:abc@unq.gbl.spaces")  # simulate the create response

    assert chat.resource_path.to_url() == "/chats/19:abc@unq.gbl.spaces"
    assert chat.members.resource_path.to_url() == "/chats/19:abc@unq.gbl.spaces/members"
    assert chat.messages.resource_path.to_url() == "/chats/19:abc@unq.gbl.spaces/messages"
