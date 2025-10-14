from typing import Optional

from office365.sharepoint.entity import Entity


class GroupMoveJobEntityData(Entity):

    @property
    def group_name(self) -> Optional[str]:
        """Gets the GroupName property"""
        return self.properties.get("GroupName", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GroupMoveJobEntityData"
