from office365.runtime.client_value import ClientValue


class SPOSiteCreationSource(ClientValue):
    def __init__(self, display_name: str = None, id_: str = None, name: str = None):
        self.DisplayName = display_name
        self.Id = id_
        self.Name = name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSiteCreationSource"
