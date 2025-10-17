from typing import Optional

from office365.sharepoint.entity import Entity


class LobSystem(Entity):

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.LobSystem"
