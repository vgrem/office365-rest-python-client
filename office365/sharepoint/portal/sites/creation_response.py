from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus


class SPSiteCreationResponse(ClientValue):
    def __init__(self, site_id: str = None, site_status: SiteStatus = None, site_url: str = None) -> None:
        super().__init__()
        self.SiteId = site_id
        self.SiteStatus = site_status
        self.SiteUrl = site_url

    def __repr__(self) -> str:
        return (
            f"SPSiteCreationResponse("
            f"site_id={self.SiteId!r}, "
            f"site_status={self.SiteStatus!r}, "
            f"site_url={self.SiteUrl!r})"
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SPSiteCreationResponse"
