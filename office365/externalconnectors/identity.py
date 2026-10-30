from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.externalconnectors.identity_type import IdentityType
from office365.runtime.types.odata_property import odata


class Identity(Entity):
    @odata(name="type")
    @property
    def type(self) -> Optional[IdentityType]:
        """Gets the type property"""
        return self.properties.get("type", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.Identity"
