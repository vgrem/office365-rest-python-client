from office365.runtime.client_value import ClientValue


class PublishSiteInformation(ClientValue):

    def __init__(self, site_type: int = None, site_url: str = None, title: str = None):
        self.SiteType = site_type
        self.SiteUrl = site_url
        self.Title = title
