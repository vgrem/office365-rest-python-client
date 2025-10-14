from typing import Optional

from office365.sharepoint.entity import Entity


class MoveSiteROStateEntity(Entity):

    @property
    def is_original_read_only(self) -> Optional[bool]:
        """Gets the IsOriginalReadOnly property"""
        return self.properties.get("IsOriginalReadOnly", None)

    @property
    def site_id(self) -> Optional[str]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.MoveSiteROStateEntity"
