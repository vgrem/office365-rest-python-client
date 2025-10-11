from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPORestrictedContentDiscoverabilitySiteDetails(ClientValue):

    def __init__(
        self,
        last_modified: datetime = None,
        site_owner_email: str = None,
        site_title: str = None,
        site_url: str = None,
        time_created: datetime = None,
    ):
        self.LastModified = last_modified
        self.SiteOwnerEmail = site_owner_email
        self.SiteTitle = site_title
        self.SiteUrl = site_url
        self.TimeCreated = time_created

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedContentDiscoverabilitySiteDetails"
