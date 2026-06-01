from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.onedrive.filestorage.access_action import AccessAction
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class ItemActivity(Entity):
    """
    The itemActivity resource provides information about activities that took place on an item or within a container.
    Currently only available on SharePoint and OneDrive for Business.
    """

    @property
    def actor(self) -> IdentitySet:
        """Identity of who performed the action."""
        return self.properties.get("actor", IdentitySet())

    @odata(name="driveItem")
    @property
    def drive_item(self):
        """Exposes the driveItem that was the target of this activity."""
        from office365.onedrive.driveitems.driveItem import DriveItem

        return self.properties.get("driveItem", DriveItem(self.context, ResourcePath("driveItem", self.resource_path)))

    @property
    def access(self) -> AccessAction:
        """Gets the access property"""
        return self.properties.get("access", AccessAction())

    @property
    def activity_date_time(self) -> datetime:
        """Gets the activityDateTime property"""
        return self.properties.get("activityDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ItemActivity"
