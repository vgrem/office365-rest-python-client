from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPORestrictedContentDiscoverabilitySiteDetails(ClientValue):
    def __init__(
        self,
        last_modified: Optional[datetime] = None,
        site_owner_email: Optional[str] = None,
        site_title: Optional[str] = None,
        site_url: Optional[str] = None,
        time_created: Optional[datetime] = None,
    ):
        self.LastModified = last_modified
        self.SiteOwnerEmail = site_owner_email
        self.SiteTitle = site_title
        self.SiteUrl = site_url
        self.TimeCreated = time_created

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedContentDiscoverabilitySiteDetails"
