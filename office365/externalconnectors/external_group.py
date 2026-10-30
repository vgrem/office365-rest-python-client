from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.externalconnectors.identity import Identity


class ExternalGroup(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalGroup"

    @odata(name="members", navigation=True)
    @property
    def members(self) -> EntityCollection[Identity]:
        """Gets the members property"""
        from office365.externalconnectors.identity import Identity

        return self.properties.get(
            "members", EntityCollection[Identity](self.context, Identity, ResourcePath("members", self.resource_path))
        )
