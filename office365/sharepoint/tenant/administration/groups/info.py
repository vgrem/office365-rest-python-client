from office365.runtime.client_value import ClientValue


class GroupInfo(ClientValue):
    def __init__(self, group_status_in_aad: int = None, site_url: str = None):
        self.GroupStatusInAAD = group_status_in_aad
        self.SiteUrl = site_url

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.GroupInfo"
