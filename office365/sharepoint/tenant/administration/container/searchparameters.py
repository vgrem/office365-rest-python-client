from office365.runtime.client_value import ClientValue


class SPContainerSearchParameters(ClientValue):

    def __init__(self, search_text: str = None):
        self.SearchText = search_text

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerSearchParameters"
