from office365.runtime.client_value import ClientValue


class AppUpgradeAvailability(ClientValue):
    def __init__(self, asset_id: str = None, is_upgrade_available: bool = None):
        self.AssetId = asset_id
        self.IsUpgradeAvailable = is_upgrade_available

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.AppUpgradeAvailability"
