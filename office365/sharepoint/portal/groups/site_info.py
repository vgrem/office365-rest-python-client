from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus


class GroupSiteInfo(ClientValue):
    def __init__(self, site_url=None, site_status: SiteStatus = None):
        """
        :param str site_url: Site url
        :param int site_status: Site status
        """
        super().__init__()
        self.SiteStatus = site_status
        self.SiteUrl = site_url
        self.DocumentsUrl = None
        self.ErrorMessage = None
        self.GroupId = None
