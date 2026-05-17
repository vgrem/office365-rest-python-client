from typing import Optional

from office365.runtime.client_value import ClientValue


class MissingLinkReferrer(ClientValue):
    def __init__(self, title: Optional[str] = None, url: Optional[str] = None):
        self.Title = title
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.MissingLinkReferrer"
