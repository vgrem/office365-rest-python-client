from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class WindowsUpdateRolloutSettings(ClientValue):
    offerEndDateTimeInUTC: datetime | None = None
    offerIntervalInDays: int | None = None
    offerStartDateTimeInUTC: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsUpdateRolloutSettings"
