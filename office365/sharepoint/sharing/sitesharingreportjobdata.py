from office365.runtime.client_value import ClientValue


class SiteSharingReportJobData(ClientValue):
    def __init__(self, folder_url: str = None, web_url: str = None):
        self.folderUrl = folder_url
        self.webUrl = web_url

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportJobData"
