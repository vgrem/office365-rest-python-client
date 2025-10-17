from typing import Optional

from office365.sharepoint.entity import Entity


class EntityIdentifier(Entity):

    @property
    def identifier_type(self) -> Optional[str]:
        """Gets the IdentifierType property"""
        return self.properties.get("IdentifierType", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.EntityIdentifier"
