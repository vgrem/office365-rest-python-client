from office365.runtime.client_value import ClientValue


class CopilotTransitiveSharingStatusItem(ClientValue):

    def __init__(
        self,
        list_id: str = None,
        site_id: str = None,
        status: int = None,
        unique_id: str = None,
        url: str = None,
        web_id: str = None,
    ):
        self.ListId = list_id
        self.SiteId = site_id
        self.Status = status
        self.UniqueId = unique_id
        self.Url = url
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotTransitiveSharingStatusItem"
