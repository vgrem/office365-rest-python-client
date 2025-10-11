from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class SyntexPremiumFeatureSettings(ClientValue):

    def __init__(
        self,
        site_list: GuidCollection = GuidCollection(),
        site_list_file_name: str = None,
        status: int = None,
    ):
        self.SiteList = site_list
        self.SiteListFileName = site_list_file_name
        self.Status = status

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexPremiumFeatureSettings"
