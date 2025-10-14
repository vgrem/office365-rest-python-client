from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class SiteAtTargetEntityData(Entity):

    @property
    def normalized_content_db_id_at_source(self) -> Optional[str]:
        """Gets the NormalizedContentDBIdAtSource property"""
        return self.properties.get("NormalizedContentDBIdAtSource", None)

    @property
    def normalized_content_db_id_at_target(self) -> Optional[str]:
        """Gets the NormalizedContentDBIdAtTarget property"""
        return self.properties.get("NormalizedContentDBIdAtTarget", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.SiteAtTargetEntityData"
