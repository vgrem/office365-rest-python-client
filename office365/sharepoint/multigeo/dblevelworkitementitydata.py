from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class DBLevelWorkItemEntityData(Entity):
    @property
    def item_guid(self) -> Optional[UUID]:
        """Gets the ItemGuid property"""
        return self.properties.get("ItemGuid", None)

    @property
    def normalized_database_id(self) -> Optional[str]:
        """Gets the NormalizedDatabaseId property"""
        return self.properties.get("NormalizedDatabaseId", None)

    @property
    def scenario_sub_type(self) -> Optional[UUID]:
        """Gets the ScenarioSubType property"""
        return self.properties.get("ScenarioSubType", None)

    @property
    def scenario_type(self) -> Optional[UUID]:
        """Gets the ScenarioType property"""
        return self.properties.get("ScenarioType", None)

    @property
    def site_subscription_id(self) -> Optional[UUID]:
        """Gets the SiteSubscriptionId property"""
        return self.properties.get("SiteSubscriptionId", None)

    @property
    def text_payload(self) -> Optional[str]:
        """Gets the TextPayload property"""
        return self.properties.get("TextPayload", None)

    @property
    def work_item_id(self) -> Optional[UUID]:
        """Gets the WorkItemId property"""
        return self.properties.get("WorkItemId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.DBLevelWorkItemEntityData"
