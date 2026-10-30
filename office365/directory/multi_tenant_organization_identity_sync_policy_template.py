from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.applications.templateapplicationlevel import TemplateApplicationLevel
from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.crosstenant.user_sync_inbound import (
        CrossTenantUserSyncInbound,
    )


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
        from office365.directory.policies.crosstenant.user_sync_inbound import (
            CrossTenantUserSyncInbound,
        )

        return self.properties.get("userSyncInbound", CrossTenantUserSyncInbound())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantOrganizationIdentitySyncPolicyTemplate"
