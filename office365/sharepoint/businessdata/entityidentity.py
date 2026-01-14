from typing import Optional

from office365.sharepoint.entity import Entity


class EntityIdentity(Entity):
    @property
    def identifier_count(self) -> Optional[int]:
        """Gets the IdentifierCount property"""
        return self.properties.get("IdentifierCount", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.Runtime.EntityIdentity"
