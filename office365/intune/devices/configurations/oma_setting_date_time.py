from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class OmaSettingDateTime(ClientValue):
    value: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OmaSettingDateTime"
