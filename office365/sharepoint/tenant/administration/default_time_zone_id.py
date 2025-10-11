from office365.runtime.client_value import ClientValue


class TenantDefaultTimeZoneId(ClientValue):

    def __init__(self, is_read_only: bool = None, value: int = None):
        self.IsReadOnly = is_read_only
        self.Value = value

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.TenantDefaultTimeZoneId"
