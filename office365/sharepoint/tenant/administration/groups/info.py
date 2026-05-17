from typing import Optional

from office365.runtime.client_value import ClientValue


class GroupInfo(ClientValue):
    def __init__(self, group_status_in_aad: Optional[int] = None, site_url: Optional[str] = None):
        self.GroupStatusInAAD = group_status_in_aad
        self.SiteUrl = site_url

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.GroupInfo"
