from __future__ import annotations

from office365.intune.devices.configurations.settingsourcetype import SettingSourceType
from office365.runtime.client_value import ClientValue


class SettingSource(ClientValue):
    displayName: str | None = None
    id: str | None = None
    sourceType: SettingSourceType = SettingSourceType.deviceConfiguration

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SettingSource"
