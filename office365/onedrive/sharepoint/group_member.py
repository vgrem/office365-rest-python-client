from __future__ import annotations

from office365.entity import Entity
from office365.onedrive.permissions.sharepoint_identity_set import SharePointIdentitySet


class SharePointGroupMember(Entity):
    @property
    def identity(self) -> SharePointIdentitySet:
        """Gets the identity property"""
        return self.properties.get("identity", SharePointIdentitySet())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointGroupMember"
