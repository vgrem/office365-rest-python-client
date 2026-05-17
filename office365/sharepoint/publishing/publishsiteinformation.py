from typing import Optional

from office365.runtime.client_value import ClientValue


class PublishSiteInformation(ClientValue):
    def __init__(self, site_type: Optional[int] = None, site_url: Optional[str] = None, title: Optional[str] = None):
        self.SiteType = site_type
        self.SiteUrl = site_url
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishSiteInformation"
