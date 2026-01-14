from office365.runtime.client_value import ClientValue


class StoreAppCreationInformation(ClientValue):
    def __init__(
        self,
        icon_url: str = None,
        publisher: str = None,
        short_description: str = None,
        store_asset_id: str = None,
    ):
        self.IconUrl = icon_url
        self.Publisher = publisher
        self.ShortDescription = short_description
        self.StoreAssetId = store_asset_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.StoreAppCreationInformation"
