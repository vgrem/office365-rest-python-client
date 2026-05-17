from typing import Optional

from office365.runtime.client_value import ClientValue


class SPOSiteCreationSource(ClientValue):
    def __init__(self, display_name: Optional[str] = None, id_: Optional[str] = None, name: Optional[str] = None):
        self.DisplayName = display_name
        self.Id = id_
        self.Name = name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSiteCreationSource"
