from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.analytics.item_activity_stat import ItemActivityStat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class ItemAnalytics(Entity):
    """The itemAnalytics resource provides analytics about activities that took place on an item.
    This resource is currently only available on SharePoint and OneDrive for Business.
    """

    @odata(name="allTime", navigation=True)
    @property
    def all_time(self) -> ItemActivityStat:
        """Analytics over the item's lifespan."""
        return self.properties.get(
            "allTime",
            ItemActivityStat(self.context, ResourcePath("allTime", self.resource_path)),
        )

    @odata(name="itemActivityStats", navigation=True)
    @property
    def item_activity_stats(self) -> EntityCollection[ItemActivityStat]:
        return self.properties.get(
            "itemActivityStats",
            EntityCollection(
                self.context,
                ItemActivityStat,
                ResourcePath("itemActivityStats", self.resource_path),
            ),
        )

    @odata(name="lastSevenDays", navigation=True)
    @property
    def last_seven_days(self) -> ItemActivityStat:
        """Analytics for the last seven days."""
        return self.properties.get(
            "lastSevenDays",
            ItemActivityStat(self.context, ResourcePath("lastSevenDays", self.resource_path)),
        )
