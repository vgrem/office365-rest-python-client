from typing import Optional

from office365.runtime.client_value import ClientValue


class CopilotTransitiveSharingStatusItem(ClientValue):
    def __init__(
        self,
        list_id: Optional[str] = None,
        site_id: Optional[str] = None,
        status: Optional[int] = None,
        unique_id: Optional[str] = None,
        url: Optional[str] = None,
        web_id: Optional[str] = None,
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
