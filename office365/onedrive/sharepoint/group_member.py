from __future__ import annotations

from office365.entity import Entity
from office365.onedrive.permissions.sharepoint_identity_set import SharePointIdentitySet
from office365.runtime.types.odata_property import odata


class SharePointGroupMember(Entity):
    @odata(name="identity")
    @property
    def identity(self) -> SharePointIdentitySet:
        """Gets the identity property"""
        return self.properties.get("identity", SharePointIdentitySet())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointGroupMember"
