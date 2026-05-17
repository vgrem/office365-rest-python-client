from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteInfoForSitePicker(ClientValue):
    def __init__(
        self,
        Error: Optional[str] = None,
        site_id: Optional[str] = None,
        site_name: Optional[str] = None,
        Url: Optional[str] = None,
        error: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        self.Error = Error
        self.SiteId = site_id
        self.SiteName = site_name
        self.Url = Url
        self.Error = error
        self.Url = url

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteInfoForSitePicker"
