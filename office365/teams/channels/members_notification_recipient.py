from __future__ import annotations

from office365.teams.teamwork.notification_recipient import TeamworkNotificationRecipient


class ChannelMembersNotificationRecipient(TeamworkNotificationRecipient):
    channelId: str | None = None
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChannelMembersNotificationRecipient"
