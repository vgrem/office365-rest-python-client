from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SyntexFeatureScopeSettingsValues(ClientValue):
    Enabled: bool | None = None
    FileName: str | None = None
    SiteScopingMode: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexFeatureScopeSettingsValues"
