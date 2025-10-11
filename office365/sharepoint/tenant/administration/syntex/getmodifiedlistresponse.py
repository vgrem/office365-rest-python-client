from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class SyntexGetModifiedListResponse(ClientValue):

    def __init__(
        self,
        ignored_urls_list: StringCollection = StringCollection(),
        modified_selected_sites_list: GuidCollection = GuidCollection(),
    ):
        self.IgnoredUrlsList = ignored_urls_list
        self.ModifiedSelectedSitesList = modified_selected_sites_list

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexGetModifiedListResponse"
