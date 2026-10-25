from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ShortcutTargetInfo(Entity):
    @odata(name="siteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the siteId property"""
        return self.properties.get("siteId", None)

    @odata(name="uniqueId")
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the uniqueId property"""
        return self.properties.get("uniqueId", None)

    @odata(name="url")
    @property
    def url(self) -> Optional[str]:
        """Gets the url property"""
        return self.properties.get("url", None)

    @odata(name="webId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the webId property"""
        return self.properties.get("webId", None)

    @property
    def entity_type_name(self):
        return "SP.Utilities.ShortcutTargetInfo"
