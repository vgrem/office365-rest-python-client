from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPOWebAppServicePrincipalPermissionRequest(Entity):
    """ """

    @odata(name="ClientComponentItemUniqueId")
    @property
    def client_component_item_unique_id(self) -> Optional[str]:
        return self.properties.get("ClientComponentItemUniqueId", False)

    @odata(name="IsDomainIsolated")
    @property
    def is_domain_isolated(self) -> Optional[bool]:
        return self.properties.get("IsDomainIsolated", False)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.Internal.SPOWebAppServicePrincipalPermissionRequest"

    @odata(name="Id")
    @property
    def id_(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="IsolatedDomainUrl")
    @property
    def isolated_domain_url(self) -> Optional[str]:
        """Gets the IsolatedDomainUrl property"""
        return self.properties.get("IsolatedDomainUrl", None)

    @odata(name="IsPreauthorizedPermission")
    @property
    def is_preauthorized_permission(self) -> Optional[bool]:
        """Gets the IsPreauthorizedPermission property"""
        return self.properties.get("IsPreauthorizedPermission", None)

    @odata(name="MultiTenantAppId")
    @property
    def multi_tenant_app_id(self) -> Optional[str]:
        """Gets the MultiTenantAppId property"""
        return self.properties.get("MultiTenantAppId", None)

    @odata(name="MultiTenantAppReplyUrl")
    @property
    def multi_tenant_app_reply_url(self) -> Optional[str]:
        """Gets the MultiTenantAppReplyUrl property"""
        return self.properties.get("MultiTenantAppReplyUrl", None)

    @odata(name="PackageApproverName")
    @property
    def package_approver_name(self) -> Optional[str]:
        """Gets the PackageApproverName property"""
        return self.properties.get("PackageApproverName", None)

    @odata(name="PackageName")
    @property
    def package_name(self) -> Optional[str]:
        """Gets the PackageName property"""
        return self.properties.get("PackageName", None)

    @odata(name="PackageVersion")
    @property
    def package_version(self) -> Optional[str]:
        """Gets the PackageVersion property"""
        return self.properties.get("PackageVersion", None)

    @odata(name="Resource")
    @property
    def resource(self) -> Optional[str]:
        """Gets the Resource property"""
        return self.properties.get("Resource", None)

    @odata(name="ResourceId")
    @property
    def resource_id(self) -> Optional[str]:
        """Gets the ResourceId property"""
        return self.properties.get("ResourceId", None)

    @odata(name="Scope")
    @property
    def scope(self) -> Optional[str]:
        """Gets the Scope property"""
        return self.properties.get("Scope", None)

    @odata(name="TimeRequested")
    @property
    def time_requested(self) -> Optional[datetime]:
        """Gets the TimeRequested property"""
        return self.properties.get("TimeRequested", datetime.min)

    def deny(self) -> Self:
        """Deny operation."""
        qry = ServiceOperationQuery(self, "Deny", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
