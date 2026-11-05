from __future__ import annotations

from datetime import timedelta

from office365.runtime.client_value import ClientValue


class OcrSettings(ClientValue):
    isEnabled: bool | None = None
    maxImageSize: int | None = None
    timeout: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.OcrSettings"
