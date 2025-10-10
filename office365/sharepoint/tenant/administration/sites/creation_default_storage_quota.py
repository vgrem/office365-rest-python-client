from office365.runtime.client_value import ClientValue


class SiteCreationDefaultStorageQuota(ClientValue):

    def __init__(
        self,
        IsReadOnly: bool = None,
        Value: int = None,
        is_read_only: bool = None,
        value: int = None,
    ) -> None:
        self.IsReadOnly = IsReadOnly
        self.Value = Value
        self.IsReadOnly = is_read_only
        self.Value = value

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationDefaultStorageQuota"
