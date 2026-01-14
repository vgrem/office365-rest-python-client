from office365.runtime.client_value import ClientValue


class SPAddinPrincipalInfo(ClientValue):
    def __init__(
        self,
        absolute_url: str = None,
        app_identifier: str = None,
        server_relative_url: str = None,
        title: str = None,
    ):
        self.absoluteUrl = absolute_url
        self.appIdentifier = app_identifier
        self.serverRelativeUrl = server_relative_url
        self.title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPrincipalInfo"
