from office365.runtime.client_value import ClientValue


class SPErrorWithServerRelativeUrl(ClientValue):
    def __init__(self, error_message: str = None, server_relative_url: str = None):
        self.errorMessage = error_message
        self.serverRelativeUrl = server_relative_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPErrorWithServerRelativeUrl"
