from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SettingDataProperty(ClientValue):
    AvailableInGraph: bool | None = None
    AvailableInPowerShell: bool | None = None
    AvailableInSharePointAdminCenter: bool | None = None
    Category: int | None = None
    Description: str | None = None
    SettingName: str | None = None
    SettingValue: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SettingDataProperty"
