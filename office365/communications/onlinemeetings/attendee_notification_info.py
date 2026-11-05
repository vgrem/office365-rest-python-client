from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AttendeeNotificationInfo(ClientValue):
    phoneNumber: str | None = None
    timeZone: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttendeeNotificationInfo"
