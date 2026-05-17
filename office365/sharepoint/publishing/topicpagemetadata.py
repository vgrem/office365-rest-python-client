from typing import Optional

from office365.sharepoint.entity import Entity


class TopicPageMetadata(Entity):
    @property
    def entity_id(self) -> Optional[str]:
        """Gets the EntityId property"""
        return self.properties.get("EntityId", None)

    @property
    def entity_type(self) -> Optional[str]:
        """Gets the EntityType property"""
        return self.properties.get("EntityType", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.TopicPageMetadata"
