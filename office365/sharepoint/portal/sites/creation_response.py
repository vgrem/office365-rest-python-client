from office365.runtime.client_value import ClientValue


class SPSiteCreationResponse(ClientValue):
    def __init__(
        self, site_id: str = None, site_status: int = None, site_url: str = None
    ) -> None:
        super(SPSiteCreationResponse, self).__init__()
        self.SiteId = site_id
        self.SiteStatus = site_status
        self.SiteUrl = site_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SPSiteCreationResponse"
