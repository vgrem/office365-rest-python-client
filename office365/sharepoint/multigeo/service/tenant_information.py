from __future__ import annotations

from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TenantInformation(Entity):
    """ """

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.TenantInformation"

    @odata(name="GeoLocation")
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @odata(name="IsIBEnabled")
    @property
    def is_ib_enabled(self) -> Optional[bool]:
        """Gets the IsIBEnabled property"""
        return self.properties.get("IsIBEnabled", None)

    @odata(name="MySiteHostDomain")
    @property
    def my_site_host_domain(self) -> Optional[str]:
        """Gets the MySiteHostDomain property"""
        return self.properties.get("MySiteHostDomain", None)

    @odata(name="PortalDomain")
    @property
    def portal_domain(self) -> Optional[str]:
        """Gets the PortalDomain property"""
        return self.properties.get("PortalDomain", None)

    @odata(name="RootSiteDomain")
    @property
    def root_site_domain(self) -> Optional[str]:
        """Gets the RootSiteDomain property"""
        return self.properties.get("RootSiteDomain", None)

    @odata(name="TenantAdminDomain")
    @property
    def tenant_admin_domain(self) -> Optional[str]:
        """Gets the TenantAdminDomain property"""
        return self.properties.get("TenantAdminDomain", None)

    @odata(name="VanityDomains")
    @property
    def vanity_domains(self) -> StringCollection:
        """Gets the VanityDomains property"""
        return self.properties.get("VanityDomains", StringCollection())
