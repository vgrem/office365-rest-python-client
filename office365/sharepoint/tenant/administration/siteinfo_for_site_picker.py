from office365.runtime.client_value import ClientValue


class SiteInfoForSitePicker(ClientValue):

    def __init__(
        self,
        Error: str = None,
        site_id: str = None,
        site_name: str = None,
        Url: str = None,
        error: str = None,
        url: str = None,
    ) -> None:
        self.Error = Error
        self.SiteId = site_id
        self.SiteName = site_name
        self.Url = Url
        self.Error = error
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteInfoForSitePicker"
