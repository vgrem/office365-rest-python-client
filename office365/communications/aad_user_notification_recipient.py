from __future__ import annotations

from office365.teams.teamwork.notification_recipient import TeamworkNotificationRecipient


class AadUserNotificationRecipient(TeamworkNotificationRecipient):
    userId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AadUserNotificationRecipient"
