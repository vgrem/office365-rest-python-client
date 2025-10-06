from office365.runtime.client_value import ClientValue


class SPStoreAppRequestInformation(ClientValue):

    def __init__(
        self,
        asset_id: str = None,
        billing_market: str = None,
        content_market: str = None,
        installation_site_id: str = None,
        installation_web_id: str = None,
        justification: str = None,
        request_type: str = None,
    ):
        self.AssetId = asset_id
        self.BillingMarket = billing_market
        self.ContentMarket = content_market
        self.InstallationSiteId = installation_site_id
        self.InstallationWebId = installation_web_id
        self.Justification = justification
        self.RequestType = request_type

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPStoreAppRequestInformation"
