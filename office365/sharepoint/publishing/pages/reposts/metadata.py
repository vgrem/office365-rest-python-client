from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.publishing.pages.metadata import SitePageMetadata


class RepostPageMetadata(SitePageMetadata):
    """"""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "SP.Publishing.RepostPageMetadata"

    @odata(name="OriginalSourceItemId")
    @property
    def original_source_item_id(self) -> Optional[UUID]:
        """Gets the OriginalSourceItemId property"""
        return self.properties.get("OriginalSourceItemId", None)

    @odata(name="OriginalSourceListId")
    @property
    def original_source_list_id(self) -> Optional[UUID]:
        """Gets the OriginalSourceListId property"""
        return self.properties.get("OriginalSourceListId", None)

    @odata(name="OriginalSourceSiteId")
    @property
    def original_source_site_id(self) -> Optional[UUID]:
        """Gets the OriginalSourceSiteId property"""
        return self.properties.get("OriginalSourceSiteId", None)

    @odata(name="OriginalSourceUrl")
    @property
    def original_source_url(self) -> Optional[str]:
        """Gets the OriginalSourceUrl property"""
        return self.properties.get("OriginalSourceUrl", None)

    @odata(name="OriginalSourceWebId")
    @property
    def original_source_web_id(self) -> Optional[UUID]:
        """Gets the OriginalSourceWebId property"""
        return self.properties.get("OriginalSourceWebId", None)
