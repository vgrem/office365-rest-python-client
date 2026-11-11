from __future__ import annotations

from typing_extensions import Self

from office365.directory.applications.templateapplicationlevel import TemplateApplicationLevel
from office365.directory.policies.crosstenant.user_sync_inbound import CrossTenantUserSyncInbound
from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class MultiTenantOrganizationIdentitySyncPolicyTemplate(Entity):
    @odata(name="templateApplicationLevel")
    @property
    def template_application_level(self) -> TemplateApplicationLevel:
        """Gets the templateApplicationLevel property"""
        return self.properties.get("templateApplicationLevel", TemplateApplicationLevel.none)

    @odata(name="userSyncInbound")
    @property
    def user_sync_inbound(self) -> CrossTenantUserSyncInbound:
        """Gets the userSyncInbound property"""
        return self.properties.get("userSyncInbound", CrossTenantUserSyncInbound())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantOrganizationIdentitySyncPolicyTemplate"

    @require_permission(
        delegated=["Policy.ReadWrite.CrossTenantAccess"],
        application=["Policy.ReadWrite.CrossTenantAccess"],
    )
    def reset_to_default_settings(self) -> Self:
        """resetToDefaultSettings operation."""
        qry = ServiceOperationQuery(self, "resetToDefaultSettings", None, {}, None, None)
        self.context.add_query(qry)
        return self
