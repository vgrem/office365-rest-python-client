from __future__ import annotations

from office365.intune.devices.configurations.oma_setting import OmaSetting


class OmaSettingInteger(OmaSetting):
    value: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OmaSettingInteger"
