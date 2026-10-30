from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.verified_id_profile import VerifiedIdProfile


class IdentityVerifiedIdRoot(Entity):
    @odata(name="profiles", navigation=True)
    @property
    def profiles(self) -> EntityCollection[VerifiedIdProfile]:
        """Gets the profiles property"""
        from office365.directory.verified_id_profile import VerifiedIdProfile

        return self.properties.get(
            "profiles",
            EntityCollection[VerifiedIdProfile](
                self.context, VerifiedIdProfile, ResourcePath("profiles", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IdentityVerifiedIdRoot"
