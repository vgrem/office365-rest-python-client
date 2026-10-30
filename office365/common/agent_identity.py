from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.objects.object import DirectoryObject


class AgentIdentity(Entity):
    @odata(name="agentIdentityBlueprintId")
    @property
    def agent_identity_blueprint_id(self) -> Optional[str]:
        """Gets the agentIdentityBlueprintId property"""
        return self.properties.get("agentIdentityBlueprintId", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="managerApplications", readonly=True)
    @property
    def manager_applications(self) -> GuidCollection:
        """Gets the managerApplications property"""
        return self.properties.get("managerApplications", GuidCollection())

    @odata(name="sponsors", navigation=True)
    @property
    def sponsors(self) -> EntityCollection[DirectoryObject]:
        """Gets the sponsors property"""
        from office365.directory.objects.object import DirectoryObject

        return self.properties.get(
            "sponsors",
            EntityCollection[DirectoryObject](
                self.context, DirectoryObject, ResourcePath("sponsors", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AgentIdentity"
