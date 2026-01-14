from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class SPUninstallAddinRequest(ClientValue):
    def __init__(
        self,
        app_instance_ids: GuidCollection = GuidCollection(),
        server_relative_url: str = None,
        url: str = None,
    ):
        self.appInstanceIds = app_instance_ids
        self.serverRelativeUrl = server_relative_url
        self.url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinRequest"
