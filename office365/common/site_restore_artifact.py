from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SiteRestoreArtifact(Entity):
    @odata(name="restoredSiteId")
    @property
    def restored_site_id(self) -> Optional[str]:
        """Gets the restoredSiteId property"""
        return self.properties.get("restoredSiteId", None)

    @odata(name="restoredSiteName", readonly=True)
    @property
    def restored_site_name(self) -> Optional[str]:
        """Gets the restoredSiteName property"""
        return self.properties.get("restoredSiteName", None)

    @odata(name="restoredSiteWebUrl", readonly=True)
    @property
    def restored_site_web_url(self) -> Optional[str]:
        """Gets the restoredSiteWebUrl property"""
        return self.properties.get("restoredSiteWebUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SiteRestoreArtifact"
