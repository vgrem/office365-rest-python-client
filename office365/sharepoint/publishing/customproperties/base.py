from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class BaseCustomProperty(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.BaseCustomProperty"

    @odata(name="IsEdited")
    @property
    def is_edited(self) -> Optional[bool]:
        """Gets the IsEdited property"""
        return self.properties.get("IsEdited", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="PropertyType")
    @property
    def property_type(self) -> Optional[str]:
        """Gets the PropertyType property"""
        return self.properties.get("PropertyType", None)
