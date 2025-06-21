from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.analytics.item_action_stat import ItemActionStat
from office365.onedrive.analytics.item_activity import ItemActivity
from office365.runtime.paths.resource_path import ResourcePath


class ItemActivityStat(Entity):
    """The itemActivityStat resource provides information about activities that took place
    within an interval of time."""

    @property
    def access(self) -> ItemActionStat:
        """Statistics about the access actions in this interval."""
        return self.properties.get("access", ItemActionStat())

    @property
    def create(self) -> ItemActionStat:
        """Statistics about the create actions in this interval."""
        return self.properties.get("create", ItemActionStat())

    @property
    def delete(self) -> ItemActionStat:
        """Statistics about the delete actions in this interval."""
        return self.properties.get("delete", ItemActionStat())

    @property
    def edit(self) -> ItemActionStat:
        """Statistics about the edit actions in this interval."""
        return self.properties.get("edit", ItemActionStat())

    @property
    def end_datetime(self) -> datetime:
        """When the interval ends. Read-only."""
        return self.properties.get("endDateTime", datetime.min)

    @property
    def is_trending(self) -> Optional[bool]:
        """Indicates whether the item is trending."""
        return self.properties.get("isTrending", None)

    @property
    def move(self) -> ItemActionStat:
        """Statistics about the move actions in this interval."""
        return self.properties.get("move", ItemActionStat())

    @property
    def start_datetime(self) -> datetime:
        """When the interval starts."""
        return self.properties.get("startDateTime", datetime.min)

    @property
    def activities(self) -> EntityCollection[ItemActivity]:
        """Exposes the itemActivities represented in this itemActivityStat resource."""
        return self.properties.get(
            "activities",
            EntityCollection(
                self.context,
                ItemActivity,
                ResourcePath("activities", self.resource_path),
            ),
        )

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "endDateTime": self.end_datetime,
                "startDateTime": self.start_datetime,
            }
            default_value = property_mapping.get(name, None)
        return super(ItemActivityStat, self).get_property(name, default_value)
