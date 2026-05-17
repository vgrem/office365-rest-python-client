from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus
from typing import Optional


class GroupSiteInfo(ClientValue):
    def __init__(
        self,
        site_url=None,
        site_status: SiteStatus = SiteStatus.None_,
        documents_url: Optional[str] = None,
        error_message: Optional[str] = None,
        group_id: Optional[str] = None,
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

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupSiteInfo"
