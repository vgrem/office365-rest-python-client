from __future__ import annotations

from typing import Optional

from office365.directory.policies.crosstenant.user_sync_inbound import CrossTenantUserSyncInbound
from office365.entity import Entity
from office365.runtime.types.odata_property import key, odata


@key("tenantId")
class CrossTenantIdentitySyncPolicyPartner(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="userSyncInbound")
    @property
    def user_sync_inbound(self) -> CrossTenantUserSyncInbound:
        """Gets the userSyncInbound property"""
        return self.properties.get("userSyncInbound", CrossTenantUserSyncInbound())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantIdentitySyncPolicyPartner"
