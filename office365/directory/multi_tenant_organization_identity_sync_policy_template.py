from __future__ import annotations

from office365.directory.applications.templateapplicationlevel import TemplateApplicationLevel
from office365.directory.policies.crosstenant.user_sync_inbound import CrossTenantUserSyncInbound
from office365.entity import Entity
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
