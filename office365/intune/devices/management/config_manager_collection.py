from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class ConfigManagerCollection(Entity):
    @odata(name="collectionIdentifier")
    @property
    def collection_identifier(self) -> Optional[str]:
        """Gets the collectionIdentifier property"""
        return self.properties.get("collectionIdentifier", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="hierarchyIdentifier")
    @property
    def hierarchy_identifier(self) -> Optional[str]:
        """Gets the hierarchyIdentifier property"""
        return self.properties.get("hierarchyIdentifier", None)

    @odata(name="hierarchyName")
    @property
    def hierarchy_name(self) -> Optional[str]:
        """Gets the hierarchyName property"""
        return self.properties.get("hierarchyName", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConfigManagerCollection"
