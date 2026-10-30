from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TopicPageMetadata(Entity):
    @odata(name="EntityId", beta=True)
    @property
    def entity_id(self) -> Optional[str]:
        """Gets the EntityId property"""
        return self.properties.get("EntityId", None)

    @odata(name="EntityType", beta=True)
    @property
    def entity_type(self) -> Optional[str]:
        """Gets the EntityType property"""
        return self.properties.get("EntityType", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.TopicPageMetadata"
