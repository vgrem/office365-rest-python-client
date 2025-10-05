from office365.runtime.client_value import ClientValue


class SharePointIds(ClientValue):

    def __init__(
        self,
        hub_site_id: str = None,
        site_id: str = None,
        site_url: str = None,
        web_id: str = None,
        list_id: str = None,
        unique_id: str = None,
    ):
        self.hub_site_id = hub_site_id
        self.site_id = site_id
        self.site_url = site_url
        self.web_id = web_id
        self.listId = list_id
        self.uniqueId = unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.SharePointIds"
