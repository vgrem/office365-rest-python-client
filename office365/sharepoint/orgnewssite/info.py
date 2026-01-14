from office365.runtime.client_value import ClientValue


class OrgNewsSiteInfo(ClientValue):
    def __init__(self, site_id: str = None, url: str = None, web_id: str = None):
        self.SiteId = site_id
        self.Url = url
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.OrgNewsSite.OrgNewsSiteInfo"
