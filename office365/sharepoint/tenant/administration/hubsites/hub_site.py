from __future__ import annotations

from typing import Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class HubSite(Entity):
    """SharePoint hub sites help you meet the needs of your organization by connecting and organizing sites"""

    def __str__(self):
        return self.title or self.entity_type_name

    def __repr__(self):
        return self.site_url or self.entity_type_name

    @odata(name="ID", beta=True)
    @property
    def id(self) -> Optional[str]:
        """Gets the id of the hub site."""
        return self.properties.get("ID", None)

    @odata(name="Description", beta=True)
    @property
    def description(self) -> Optional[str]:
        """Gets the description of the hub site type."""
        return self.properties.get("Description", None)

    @odata(name="SiteUrl", beta=True)
    @property
    def site_url(self) -> Optional[str]:
        """Gets the url of the hub site."""
        return self.properties.get("SiteUrl", None)

    @odata(name="Targets", beta=True)
    @property
    def targets(self) -> Optional[str]:
        """List of security groups with access to join the hub site. Null if everyone has permission."""
        return self.properties.get("Targets", None)

    @odata(name="Title", beta=True)
    @property
    def title(self) -> Optional[str]:
        """Gets the title of the hub site."""
        return self.properties.get("Title", None)

    @odata(name="TenantInstanceId", beta=True)
    @property
    def tenant_instance_id(self) -> Optional[str]:
        """Gets The tenant instance ID in which the hub site is located."""
        return self.properties.get("TenantInstanceId", None)

    @odata(name="EnablePermissionsSync", beta=True)
    @property
    def enable_permissions_sync(self) -> Optional[bool]:
        """Gets the EnablePermissionsSync property"""
        return self.properties.get("EnablePermissionsSync", None)

    @odata(name="EnforcedECTs", beta=True)
    @property
    def enforced_ects(self) -> Optional[str]:
        """Gets the EnforcedECTs property"""
        return self.properties.get("EnforcedECTs", None)

    @odata(name="EnforcedECTsVersion", beta=True)
    @property
    def enforced_ects_version(self) -> Optional[int]:
        """Gets the EnforcedECTsVersion property"""
        return self.properties.get("EnforcedECTsVersion", None)

    @odata(name="HideNameInNavigation", beta=True)
    @property
    def hide_name_in_navigation(self) -> Optional[bool]:
        """Gets the HideNameInNavigation property"""
        return self.properties.get("HideNameInNavigation", None)

    @odata(name="LogoUrl", beta=True)
    @property
    def logo_url(self) -> Optional[str]:
        """Gets the LogoUrl property"""
        return self.properties.get("LogoUrl", None)

    @odata(name="ParentHubSiteId", beta=True)
    @property
    def parent_hub_site_id(self) -> Optional[UUID]:
        """Gets the ParentHubSiteId property"""
        return self.properties.get("ParentHubSiteId", None)

    @odata(name="PermissionsSyncTag", beta=True)
    @property
    def permissions_sync_tag(self) -> Optional[int]:
        """Gets the PermissionsSyncTag property"""
        return self.properties.get("PermissionsSyncTag", None)

    @odata(name="RequiresJoinApproval", beta=True)
    @property
    def requires_join_approval(self) -> Optional[bool]:
        """Gets the RequiresJoinApproval property"""
        return self.properties.get("RequiresJoinApproval", None)

    @odata(name="SiteDesignId", beta=True)
    @property
    def site_design_id(self) -> Optional[UUID]:
        """Gets the SiteDesignId property"""
        return self.properties.get("SiteDesignId", None)

    @odata(name="SiteId", beta=True)
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    def delete(self) -> Self:
        """Delete operation."""
        qry = ServiceOperationQuery(self, "Delete", None, {}, None, None)
        self.context.add_query(qry)
        return self
