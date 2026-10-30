from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class RemoteTenantGroup(Entity):
    @odata(name="remoteGroupDisplayName")
    @property
    def remote_group_display_name(self) -> Optional[str]:
        """Gets the remoteGroupDisplayName property"""
        return self.properties.get("remoteGroupDisplayName", None)

    @odata(name="remoteGroupId")
    @property
    def remote_group_id(self) -> Optional[UUID]:
        """Gets the remoteGroupId property"""
        return self.properties.get("remoteGroupId", None)

    @odata(name="remoteTenantDisplayName")
    @property
    def remote_tenant_display_name(self) -> Optional[str]:
        """Gets the remoteTenantDisplayName property"""
        return self.properties.get("remoteTenantDisplayName", None)

    @odata(name="remoteTenantId")
    @property
    def remote_tenant_id(self) -> Optional[UUID]:
        """Gets the remoteTenantId property"""
        return self.properties.get("remoteTenantId", None)

    @odata(name="remoteTenantPrimaryDomain")
    @property
    def remote_tenant_primary_domain(self) -> Optional[str]:
        """Gets the remoteTenantPrimaryDomain property"""
        return self.properties.get("remoteTenantPrimaryDomain", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RemoteTenantGroup"
