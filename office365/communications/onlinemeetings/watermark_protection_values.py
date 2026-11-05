from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WatermarkProtectionValues(ClientValue):
    isEnabledForContentSharing: bool | None = None
    isEnabledForVideo: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WatermarkProtectionValues"
