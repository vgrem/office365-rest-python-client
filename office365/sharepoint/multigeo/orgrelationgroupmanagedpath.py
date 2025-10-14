from typing import Optional

from office365.sharepoint.entity import Entity


class OrgRelationGroupManagedPath(Entity):

    @property
    def group_managed_path(self) -> Optional[str]:
        """Gets the GroupManagedPath property"""
        return self.properties.get("GroupManagedPath", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.OrgRelationGroupManagedPath"
