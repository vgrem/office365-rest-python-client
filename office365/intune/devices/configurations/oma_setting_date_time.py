from __future__ import annotations

from datetime import datetime

from office365.intune.devices.configurations.oma_setting import OmaSetting


class OmaSettingDateTime(OmaSetting):
    value: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OmaSettingDateTime"
