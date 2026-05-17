from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection
from typing import Optional


class SyntexPremiumFeatureSettings(ClientValue):
    def __init__(
        self,
        site_list: GuidCollection = GuidCollection(),
        site_list_file_name: Optional[str] = None,
        status: Optional[int] = None,
    ):
        self.SiteList = site_list
        self.SiteListFileName = site_list_file_name
        self.Status = status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexPremiumFeatureSettings"
