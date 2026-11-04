from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserTrainingContentEventInfo(ClientValue):
    browser: str | None = None
    contentDateTime: datetime | None = None
    ipAddress: str | None = None
    osPlatformDeviceDetails: str | None = None
    potentialScoreImpact: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserTrainingContentEventInfo"
