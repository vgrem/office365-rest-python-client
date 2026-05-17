from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteSharingReportJobData(ClientValue):
    def __init__(self, folder_url: Optional[str] = None, web_url: Optional[str] = None):
        self.folderUrl = folder_url
        self.webUrl = web_url

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportJobData"
