from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class GeoTenantInstanceInformationEntityData(Entity):

    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @property
    def instance_id(self) -> Optional[UUID]:
        """Gets the InstanceId property"""
        return self.properties.get("InstanceId", None)

    @property
    def instance_state(self) -> Optional[int]:
        """Gets the InstanceState property"""
        return self.properties.get("InstanceState", None)

    @property
    def is_current_user_geo_administrator(self) -> Optional[bool]:
        """Gets the IsCurrentUserGeoAdministrator property"""
        return self.properties.get("IsCurrentUserGeoAdministrator", None)

    @property
    def is_default_geo_location(self) -> Optional[bool]:
        """Gets the IsDefaultGeoLocation property"""
        return self.properties.get("IsDefaultGeoLocation", None)

    @property
    def my_site_host_domain(self) -> Optional[str]:
        """Gets the MySiteHostDomain property"""
        return self.properties.get("MySiteHostDomain", None)

    @property
    def odb_count(self) -> Optional[int]:
        """Gets the OdbCount property"""
        return self.properties.get("OdbCount", None)

    @property
    def portal_domain(self) -> Optional[str]:
        """Gets the PortalDomain property"""
        return self.properties.get("PortalDomain", None)

    @property
    def regular_site_count(self) -> Optional[int]:
        """Gets the RegularSiteCount property"""
        return self.properties.get("RegularSiteCount", None)

    @property
    def root_site_domain(self) -> Optional[str]:
        """Gets the RootSiteDomain property"""
        return self.properties.get("RootSiteDomain", None)

    @property
    def tenant_admin_domain(self) -> Optional[str]:
        """Gets the TenantAdminDomain property"""
        return self.properties.get("TenantAdminDomain", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoTenantInstanceInformationEntityData"
