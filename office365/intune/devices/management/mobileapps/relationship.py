from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class MobileAppRelationship(Entity):
    @property
    def source_display_name(self) -> Optional[str]:
        """Gets the sourceDisplayName property"""
        return self.properties.get("sourceDisplayName", None)

    @property
    def source_display_version(self) -> Optional[str]:
        """Gets the sourceDisplayVersion property"""
        return self.properties.get("sourceDisplayVersion", None)

    @property
    def source_id(self) -> Optional[str]:
        """Gets the sourceId property"""
        return self.properties.get("sourceId", None)

    @property
    def source_publisher_display_name(self) -> Optional[str]:
        """Gets the sourcePublisherDisplayName property"""
        return self.properties.get("sourcePublisherDisplayName", None)

    @property
    def target_display_name(self) -> Optional[str]:
        """Gets the targetDisplayName property"""
        return self.properties.get("targetDisplayName", None)

    @property
    def target_display_version(self) -> Optional[str]:
        """Gets the targetDisplayVersion property"""
        return self.properties.get("targetDisplayVersion", None)

    @property
    def target_id(self) -> Optional[str]:
        """Gets the targetId property"""
        return self.properties.get("targetId", None)

    @property
    def target_publisher_display_name(self) -> Optional[str]:
        """Gets the targetPublisherDisplayName property"""
        return self.properties.get("targetPublisherDisplayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppRelationship"
