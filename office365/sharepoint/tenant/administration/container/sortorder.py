from office365.runtime.client_value import ClientValue


class SPContainerSortOrder(ClientValue):
    def __init__(self, ascending: bool = None, sorting_field: int = None):
        self.Ascending = ascending
        self.SortingField = sorting_field

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerSortOrder"
