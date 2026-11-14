from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.teams.chats.event_message_detail import EventMessageDetail


class ChannelSetAsFavoriteByDefaultEventMessageDetail(EventMessageDetail):
    channelId: str | None = None
    initiator: IdentitySet = field(default_factory=IdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelSetAsFavoriteByDefaultEventMessageDetail"
