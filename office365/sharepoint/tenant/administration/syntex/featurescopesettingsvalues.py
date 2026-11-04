from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SyntexFeatureScopeSettingsValues(ClientValue):
    Enabled: bool | None = None
    FileName: str | None = None
    SiteScopingMode: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexFeatureScopeSettingsValues"
