from office365.runtime.client_value import ClientValue


class SPOTenantWebTemplate(ClientValue):

    def __init__(
        self,
        compatibility_level: int = None,
        description: str = None,
        display_category: str = None,
        id_: int = None,
        lcid: int = None,
        name: str = None,
        title: str = None,
    ):
        super().__init__()
        self.CompatibilityLevel = compatibility_level
        self.Description = description
        self.DisplayCategory = display_category
        self.Id = id_
        self.Lcid = lcid
        self.Name = name
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOTenantWebTemplate"
