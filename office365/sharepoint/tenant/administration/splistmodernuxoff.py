from office365.runtime.client_value import ClientValue


class SPListModernUXOff(ClientValue):

    def __init__(self, is_hidden: bool = None, is_read_only: bool = None, value: bool = None):
        self.IsHidden = is_hidden
        self.IsReadOnly = is_read_only
        self.Value = value

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPListModernUXOff"
