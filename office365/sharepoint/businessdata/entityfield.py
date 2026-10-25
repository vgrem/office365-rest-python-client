from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class EntityField(Entity):
    @odata(name="ContainsLocalizedDisplayName")
    @property
    def contains_localized_display_name(self) -> Optional[bool]:
        """Gets the ContainsLocalizedDisplayName property"""
        return self.properties.get("ContainsLocalizedDisplayName", None)

    @odata(name="DefaultDisplayName")
    @property
    def default_display_name(self) -> Optional[str]:
        """Gets the DefaultDisplayName property"""
        return self.properties.get("DefaultDisplayName", None)

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

    @property
    def entity_type_name(self):
        return "SP.BusinessData.EntityField"
