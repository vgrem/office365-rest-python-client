from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.administration.hubsites.permission import (
    HubSitePermission,
)


class HubSiteProperties(Entity):
    @odata(name="Permissions")
    @property
    def permissions(self):
        return self.properties.get("Permissions", ClientValueCollection(HubSitePermission))

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[str]:
        """Returns the Site identifier"""
        return self.properties.get("SiteId", None)

    @property
    def property_ref_name(self):
        return "SiteId"

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.HubSiteProperties"

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="EnablePermissionsSync")
    @property
    def enable_permissions_sync(self) -> Optional[bool]:
        """Gets the EnablePermissionsSync property"""
        return self.properties.get("EnablePermissionsSync", None)

    @odata(name="HideNameInNavigation")
    @property
    def hide_name_in_navigation(self) -> Optional[bool]:
        """Gets the HideNameInNavigation property"""
        return self.properties.get("HideNameInNavigation", None)

    @odata(name="ID")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="LogoUrl")
    @property
    def logo_url(self) -> Optional[str]:
        """Gets the LogoUrl property"""
        return self.properties.get("LogoUrl", None)

    @odata(name="ParentHubSiteId")
    @property
    def parent_hub_site_id(self) -> Optional[UUID]:
        """Gets the ParentHubSiteId property"""
        return self.properties.get("ParentHubSiteId", None)

    @odata(name="RequiresJoinApproval")
    @property
    def requires_join_approval(self) -> Optional[bool]:
        """Gets the RequiresJoinApproval property"""
        return self.properties.get("RequiresJoinApproval", None)

    @odata(name="SiteDesignId")
    @property
    def site_design_id(self) -> Optional[UUID]:
        """Gets the SiteDesignId property"""
        return self.properties.get("SiteDesignId", None)

    @odata(name="SiteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)
