from __future__ import annotations

from office365.teams.teamwork.notification_recipient import TeamworkNotificationRecipient


class ChatMembersNotificationRecipient(TeamworkNotificationRecipient):
    chatId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMembersNotificationRecipient"
