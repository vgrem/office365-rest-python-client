from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ChannelMembersNotificationRecipient(ClientValue):
    channelId: str | None = None
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelMembersNotificationRecipient"
