from office365.sharepoint.entity import Entity


class SPMarketplaceSettings(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Marketplace.SPMarketplaceSettings"
