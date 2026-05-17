from typing import Optional

from office365.runtime.client_value import ClientValue


class SyntexFeatureScopeSettingsValues(ClientValue):
    def __init__(
        self, enabled: Optional[bool] = None, file_name: Optional[str] = None, site_scoping_mode: Optional[int] = None
    ):
        self.Enabled = enabled
        self.FileName = file_name
        self.SiteScopingMode = site_scoping_mode

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexFeatureScopeSettingsValues"
