from __future__ import annotations

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class Fido2CombinationConfiguration(Entity):
    @odata(name="allowedAAGUIDs")
    @property
    def allowed_aaguids(self) -> StringCollection:
        """Gets the allowedAAGUIDs property"""
        return self.properties.get("allowedAAGUIDs", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Fido2CombinationConfiguration"
