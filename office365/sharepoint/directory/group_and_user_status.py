from __future__ import annotations

from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.directory.groups.group import Group
from office365.sharepoint.entity import Entity


class GroupAndUserStatus(Entity):
    """ """

    @odata(name="Group", navigation=True)
    @property
    def group(self) -> Group:
        """Get a Group"""
        return self.properties.get("Group", Group(self.context, ResourcePath("Group", self.resource_path)))

    @property
    def entity_type_name(self):
        return "SP.Directory.GroupAndUserStatus"

    @odata(name="Status")
    @property
    def status(self) -> Optional[int]:
        """Gets the Status property"""
        return self.properties.get("Status", None)
