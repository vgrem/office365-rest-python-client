from typing import Optional

from office365.sharepoint.entity import Entity


class OrgRelationNotification(Entity):

    @property
    def notification_succeeded(self) -> Optional[bool]:
        """Gets the NotificationSucceeded property"""
        return self.properties.get("NotificationSucceeded", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.OrgRelationNotification"
