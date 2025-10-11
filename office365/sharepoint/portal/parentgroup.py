from office365.runtime.client_value import ClientValue


class ParentGroup(ClientValue):

    def __init__(self, display_name: str = None, group_site_url: str = None, id_: str = None):
        self.DisplayName = display_name
        self.GroupSiteUrl = group_site_url
        self.ID = id_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ParentGroup"
