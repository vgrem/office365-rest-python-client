from typing import Optional

from office365.runtime.client_value import ClientValue


class SPContainerSearchParameters(ClientValue):
    def __init__(self, search_text: Optional[str] = None):
        self.SearchText = search_text

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerSearchParameters"
