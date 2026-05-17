from office365.runtime.client_value import ClientValue
from typing import Optional


class LinkedSiteContract(ClientValue):
    def __init__(
        self,
        display_name: Optional[str] = None,
        group_id: Optional[str] = None,
        picture_url: Optional[str] = None,
        site_id: Optional[str] = None,
        url: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        self.DisplayName = display_name
        self.GroupId = group_id
        self.PictureUrl = picture_url
        self.SiteId = site_id
        self.Url = url
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.LinkedSiteContract"
