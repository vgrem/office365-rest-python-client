from office365.runtime.client_value import ClientValue


class LinkedSiteContract(ClientValue):

    def __init__(
        self,
        display_name: str = None,
        group_id: str = None,
        picture_url: str = None,
        site_id: str = None,
        url: str = None,
        web_id: str = None,
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
