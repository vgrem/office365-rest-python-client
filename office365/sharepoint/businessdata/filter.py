from typing import Optional

from office365.sharepoint.entity import Entity


class Filter(Entity):
    @property
    def default_display_name(self) -> Optional[str]:
        """Gets the DefaultDisplayName property"""
        return self.properties.get("DefaultDisplayName", None)

    @property
    def filter_field(self) -> Optional[str]:
        """Gets the FilterField property"""
        return self.properties.get("FilterField", None)

    @property
    def filter_type(self) -> Optional[str]:
        """Gets the FilterType property"""
        return self.properties.get("FilterType", None)

    @property
    def localized_display_name(self) -> Optional[str]:
        """Gets the LocalizedDisplayName property"""
        return self.properties.get("LocalizedDisplayName", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def value_count(self) -> Optional[int]:
        """Gets the ValueCount property"""
        return self.properties.get("ValueCount", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.Filter"
