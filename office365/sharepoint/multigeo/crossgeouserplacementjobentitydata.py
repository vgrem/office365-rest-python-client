from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class CrossGeoUserPlacementJobEntityData(Entity):

    @property
    def tenant_my_site_url(self) -> Optional[str]:
        """Gets the TenantMySiteUrl property"""
        return self.properties.get("TenantMySiteUrl", None)

    @property
    def user_object_id(self) -> Optional[UUID]:
        """Gets the UserObjectId property"""
        return self.properties.get("UserObjectId", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the UserPrincipalName property"""
        return self.properties.get("UserPrincipalName", None)

    @property
    def workitem_id(self) -> Optional[UUID]:
        """Gets the WorkitemId property"""
        return self.properties.get("WorkitemId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoUserPlacementJobEntityData"
