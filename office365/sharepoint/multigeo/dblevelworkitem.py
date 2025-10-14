from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class DBLevelWorkItem(Entity):

    @property
    def work_item_id(self) -> Optional[UUID]:
        """Gets the WorkItemId property"""
        return self.properties.get("WorkItemId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.DBLevelWorkItem"
