from typing import Optional

from office365.runtime.client_value import ClientValue


class TenantDefaultTimeZoneId(ClientValue):
    def __init__(self, is_read_only: Optional[bool] = None, value: Optional[int] = None):
        self.IsReadOnly = is_read_only
        self.Value = value

    " "

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.TenantDefaultTimeZoneId"
