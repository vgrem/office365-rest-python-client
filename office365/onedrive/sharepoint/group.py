from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.sharepoint.group_member import SharePointGroupMember
from office365.runtime.paths.resource_path import ResourcePath


class SharePointGroup(Entity):
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def principal_id(self) -> Optional[str]:
        """Gets the principalId property"""
        return self.properties.get("principalId", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @property
    def members(self) -> EntityCollection[SharePointGroupMember]:
        """Gets the members property"""
        return self.properties.get(
            "members",
            EntityCollection[SharePointGroupMember](
                self.context, SharePointGroupMember, ResourcePath("members", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointGroup"
