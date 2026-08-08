from __future__ import annotations

from enum import Enum


class NotificationRecipientsType(Enum):
    none = "0"
    globalAdmins = "1"
    backupAdmins = "2"
    custom = "4"
    allAdmins = "8"
    unknownFutureValue = "16"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NotificationRecipientsType"
