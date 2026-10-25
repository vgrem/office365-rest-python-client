from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class Link(Entity):
    @property
    def entity_type_name(self):
        return "SP.Directory.Link"

    @odata(name="id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @odata(name="objectSubtype")
    @property
    def object_subtype(self) -> Optional[int]:
        """Gets the objectSubtype property"""
        return self.properties.get("objectSubtype", None)

    @odata(name="objectType")
    @property
    def object_type(self) -> Optional[str]:
        """Gets the objectType property"""
        return self.properties.get("objectType", None)
