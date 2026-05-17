from typing import Optional

from office365.sharepoint.entity import Entity


class EntityView(Entity):
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def related_specific_finder_name(self) -> Optional[str]:
        """Gets the RelatedSpecificFinderName property"""
        return self.properties.get("RelatedSpecificFinderName", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.EntityView"
