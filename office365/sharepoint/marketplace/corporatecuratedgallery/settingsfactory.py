from office365.sharepoint.entity import Entity


class SPCorporateCuratedGallerySettingsFactory(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPCorporateCuratedGallerySettingsFactory"
