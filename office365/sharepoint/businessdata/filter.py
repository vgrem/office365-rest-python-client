from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class Filter(Entity):
    @odata(name="DefaultDisplayName")
    @property
    def default_display_name(self) -> Optional[str]:
        """Gets the DefaultDisplayName property"""
        return self.properties.get("DefaultDisplayName", None)

    @odata(name="FilterField")
    @property
    def filter_field(self) -> Optional[str]:
        """Gets the FilterField property"""
        return self.properties.get("FilterField", None)

    @odata(name="FilterType")
    @property
    def filter_type(self) -> Optional[str]:
        """Gets the FilterType property"""
        return self.properties.get("FilterType", None)

    @odata(name="LocalizedDisplayName")
    @property
    def localized_display_name(self) -> Optional[str]:
        """Gets the LocalizedDisplayName property"""
        return self.properties.get("LocalizedDisplayName", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="ValueCount")
    @property
    def value_count(self) -> Optional[int]:
        """Gets the ValueCount property"""
        return self.properties.get("ValueCount", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.Filter"
