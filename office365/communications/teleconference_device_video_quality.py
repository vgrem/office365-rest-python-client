from __future__ import annotations

from office365.communications.teleconference_device_media_quality import TeleconferenceDeviceMediaQuality


class TeleconferenceDeviceVideoQuality(TeleconferenceDeviceMediaQuality):
    averageInboundBitRate: float | None = None
    averageInboundFrameRate: float | None = None
    averageOutboundBitRate: float | None = None
    averageOutboundFrameRate: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeleconferenceDeviceVideoQuality"
