from __future__ import annotations

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity


class SPFarm(Entity):

    @property
    def local(self) -> SPFarm:
        """Gets the Local property"""
        return self.properties.get("Local", SPFarm(self.context, ResourcePath("Local", self.resource_path)))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.SPFarm"
