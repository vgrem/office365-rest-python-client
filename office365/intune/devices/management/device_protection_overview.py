from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DeviceProtectionOverview(ClientValue):
    cleanDeviceCount: int | None = None
    criticalFailuresDeviceCount: int | None = None
    inactiveThreatAgentDeviceCount: int | None = None
    pendingFullScanDeviceCount: int | None = None
    pendingManualStepsDeviceCount: int | None = None
    pendingOfflineScanDeviceCount: int | None = None
    pendingQuickScanDeviceCount: int | None = None
    pendingRestartDeviceCount: int | None = None
    pendingSignatureUpdateDeviceCount: int | None = None
    totalReportedDeviceCount: int | None = None
    unknownStateThreatAgentDeviceCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceProtectionOverview"
