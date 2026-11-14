from __future__ import annotations

from office365.intune.devices.configurations.oma_setting import OmaSetting


class OmaSettingStringXml(OmaSetting):
    fileName: str | None = None
    value: bytes | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OmaSettingStringXml"
