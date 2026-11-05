from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class MobileAppInstallTimeSettings(ClientValue):
    deadlineDateTime: datetime | None = None
    startDateTime: datetime | None = None
    useLocalTime: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppInstallTimeSettings"
