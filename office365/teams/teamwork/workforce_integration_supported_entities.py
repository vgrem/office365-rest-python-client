from __future__ import annotations

from enum import Enum


class WorkforceIntegrationSupportedEntities(Enum):
    none = "0"
    shift = "1"
    swapRequest = "2"
    userShiftPreferences = "8"
    openShift = "16"
    openShiftRequest = "32"
    offerShiftRequest = "64"
    unknownFutureValue = "1024"
    timeCard = "2048"
    timeOffReason = "4096"
    timeOff = "8192"
    timeOffRequest = "16384"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkforceIntegrationSupportedEntities"
