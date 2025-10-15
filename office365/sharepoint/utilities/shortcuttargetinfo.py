from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class ShortcutTargetInfo(Entity):

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the siteId property"""
        return self.properties.get("siteId", None)

    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the uniqueId property"""
        return self.properties.get("uniqueId", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the url property"""
        return self.properties.get("url", None)

    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the webId property"""
        return self.properties.get("webId", None)

    @property
    def entity_type_name(self):
        return "SP.Utilities.ShortcutTargetInfo"
