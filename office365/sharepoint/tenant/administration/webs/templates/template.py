from typing import Optional

from office365.runtime.client_value import ClientValue


class SPOTenantWebTemplate(ClientValue):
    def __init__(
        self,
        compatibility_level: Optional[int] = None,
        description: Optional[str] = None,
        display_category: Optional[str] = None,
        id_: Optional[int] = None,
        lcid: Optional[int] = None,
        name: Optional[str] = None,
        title: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOTenantWebTemplate"
