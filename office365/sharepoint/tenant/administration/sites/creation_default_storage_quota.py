from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteCreationDefaultStorageQuota(ClientValue):
    def __init__(
        self,
        IsReadOnly: Optional[bool] = None,
        Value: Optional[int] = None,
        is_read_only: Optional[bool] = None,
        value: Optional[int] = None,
    ) -> None:
        self.IsReadOnly = IsReadOnly
        self.Value = Value
        self.IsReadOnly = is_read_only
        self.Value = value

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationDefaultStorageQuota"
