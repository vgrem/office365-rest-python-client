from __future__ import annotations

from office365.intune.devices.configurations.oma_setting import OmaSetting


class OmaSettingBoolean(OmaSetting):
    value: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OmaSettingBoolean"
