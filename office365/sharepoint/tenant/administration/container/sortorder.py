from office365.runtime.client_value import ClientValue
from typing import Optional


class SPContainerSortOrder(ClientValue):
    def __init__(self, ascending: Optional[bool] = None, sorting_field: Optional[int] = None):
        self.Ascending = ascending
        self.SortingField = sorting_field

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerSortOrder"
