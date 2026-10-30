from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class ProfilePropertySetting(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="prioritizedSourceUrls")
    @property
    def prioritized_source_urls(self) -> StringCollection:
        """Gets the prioritizedSourceUrls property"""
        return self.properties.get("prioritizedSourceUrls", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProfilePropertySetting"
