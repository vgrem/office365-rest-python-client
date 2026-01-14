from typing import Optional

from office365.sharepoint.entity import Entity


class SPCorporateCuratedGallerySettingsBase(Entity):
    @property
    def host_site_full_url(self) -> Optional[str]:
        """Gets the HostSiteFullUrl property"""
        return self.properties.get("HostSiteFullUrl", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPCorporateCuratedGallerySettingsBase"
