from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class UnifiedGroup(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.UnifiedGroup"

    @odata(name="DisplayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @odata(name="GroupAlias")
    @property
    def group_alias(self) -> Optional[str]:
        """Gets the GroupAlias property"""
        return self.properties.get("GroupAlias", None)

    @odata(name="Mail")
    @property
    def mail(self) -> Optional[str]:
        """Gets the Mail property"""
        return self.properties.get("Mail", None)

    @odata(name="ObjectId")
    @property
    def object_id(self) -> Optional[UUID]:
        """Gets the ObjectId property"""
        return self.properties.get("ObjectId", None)

    @odata(name="PreferredDataLocation")
    @property
    def preferred_data_location(self) -> Optional[str]:
        """Gets the PreferredDataLocation property"""
        return self.properties.get("PreferredDataLocation", None)

    @odata(name="SiteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)
