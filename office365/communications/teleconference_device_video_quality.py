from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TeleconferenceDeviceVideoQuality(ClientValue):
    averageInboundBitRate: float | None = None
    averageInboundFrameRate: float | None = None
    averageOutboundBitRate: float | None = None
    averageOutboundFrameRate: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeleconferenceDeviceVideoQuality"
