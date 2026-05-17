from office365.runtime.client_value import ClientValue
from typing import Optional


class NewSubsiteInModernOffForModernTemplates(ClientValue):
    def __init__(self, is_read_only: Optional[bool] = None, value: Optional[bool] = None):
        self.IsReadOnly = is_read_only
        self.Value = value

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.NewSubsiteInModernOffForModernTemplates"
