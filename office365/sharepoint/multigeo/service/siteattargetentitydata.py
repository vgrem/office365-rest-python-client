from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SiteAtTargetEntityData(Entity):
    @odata(name="NormalizedContentDBIdAtSource")
    @property
    def normalized_content_db_id_at_source(self) -> Optional[str]:
        """Gets the NormalizedContentDBIdAtSource property"""
        return self.properties.get("NormalizedContentDBIdAtSource", None)

    @odata(name="NormalizedContentDBIdAtTarget")
    @property
    def normalized_content_db_id_at_target(self) -> Optional[str]:
        """Gets the NormalizedContentDBIdAtTarget property"""
        return self.properties.get("NormalizedContentDBIdAtTarget", None)

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.SiteAtTargetEntityData"
