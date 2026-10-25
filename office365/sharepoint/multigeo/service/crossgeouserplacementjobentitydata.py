from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossGeoUserPlacementJobEntityData(Entity):
    @odata(name="TenantMySiteUrl")
    @property
    def tenant_my_site_url(self) -> Optional[str]:
        """Gets the TenantMySiteUrl property"""
        return self.properties.get("TenantMySiteUrl", None)

    @odata(name="UserObjectId")
    @property
    def user_object_id(self) -> Optional[UUID]:
        """Gets the UserObjectId property"""
        return self.properties.get("UserObjectId", None)

    @odata(name="UserPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the UserPrincipalName property"""
        return self.properties.get("UserPrincipalName", None)

    @odata(name="WorkitemId")
    @property
    def workitem_id(self) -> Optional[UUID]:
        """Gets the WorkitemId property"""
        return self.properties.get("WorkitemId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoUserPlacementJobEntityData"
