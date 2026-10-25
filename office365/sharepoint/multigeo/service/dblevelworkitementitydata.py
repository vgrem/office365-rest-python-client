from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DBLevelWorkItemEntityData(Entity):
    @odata(name="ItemGuid")
    @property
    def item_guid(self) -> Optional[UUID]:
        """Gets the ItemGuid property"""
        return self.properties.get("ItemGuid", None)

    @odata(name="NormalizedDatabaseId")
    @property
    def normalized_database_id(self) -> Optional[str]:
        """Gets the NormalizedDatabaseId property"""
        return self.properties.get("NormalizedDatabaseId", None)

    @odata(name="ScenarioSubType")
    @property
    def scenario_sub_type(self) -> Optional[UUID]:
        """Gets the ScenarioSubType property"""
        return self.properties.get("ScenarioSubType", None)

    @odata(name="ScenarioType")
    @property
    def scenario_type(self) -> Optional[UUID]:
        """Gets the ScenarioType property"""
        return self.properties.get("ScenarioType", None)

    @odata(name="SiteSubscriptionId")
    @property
    def site_subscription_id(self) -> Optional[UUID]:
        """Gets the SiteSubscriptionId property"""
        return self.properties.get("SiteSubscriptionId", None)

    @odata(name="TextPayload")
    @property
    def text_payload(self) -> Optional[str]:
        """Gets the TextPayload property"""
        return self.properties.get("TextPayload", None)

    @odata(name="WorkItemId")
    @property
    def work_item_id(self) -> Optional[UUID]:
        """Gets the WorkItemId property"""
        return self.properties.get("WorkItemId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.DBLevelWorkItemEntityData"
