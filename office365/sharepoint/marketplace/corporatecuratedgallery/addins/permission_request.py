from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPAddinPermissionRequest(ClientValue):

    def __init__(
        self,
        app_identifiers: StringCollection = StringCollection(),
        server_relative_url: str = None,
        url: str = None,
    ):
        self.appIdentifiers = app_identifiers
        self.serverRelativeUrl = server_relative_url
        self.url = url

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionRequest"
