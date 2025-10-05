from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus


class GroupSiteInfo(ClientValue):

    def __init__(
        self,
        site_url=None,
        site_status: SiteStatus = None,
        documents_url: str = None,
        error_message: str = None,
        group_id: str = None,
    ):
        """
        :param str site_url: Site url
        :param int site_status: Site status
        """
        super().__init__()
        self.SiteStatus = site_status
        self.SiteUrl = site_url
        self.DocumentsUrl = documents_url
        self.ErrorMessage = error_message
        self.GroupId = group_id
