from __future__ import annotations

from office365.directory.identities.named_location import NamedLocation
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class CaPoliciesDeletableRoot(Entity):
    @odata(name="namedLocations", navigation=True)
    @property
    def named_locations(self) -> EntityCollection[NamedLocation]:
        """Gets the namedLocations property"""
        return self.properties.get(
            "namedLocations",
            EntityCollection[NamedLocation](
                self.context, NamedLocation, ResourcePath("namedLocations", self.resource_path)
            ),
        )

    @odata(name="policies", navigation=True)
    @property
    def policies(self) -> EntityCollection[ConditionalAccessPolicy]:
        """Gets the policies property"""
        return self.properties.get(
            "policies",
            EntityCollection[ConditionalAccessPolicy](
                self.context, ConditionalAccessPolicy, ResourcePath("policies", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CaPoliciesDeletableRoot"
