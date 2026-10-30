from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TenantGovernanceSetting(Entity):
    @odata(name="canReceiveInvitations")
    @property
    def can_receive_invitations(self) -> Optional[bool]:
        """Gets the canReceiveInvitations property"""
        return self.properties.get("canReceiveInvitations", None)

    @odata(name="isRelatedTenantsEnabled")
    @property
    def is_related_tenants_enabled(self) -> Optional[bool]:
        """Gets the isRelatedTenantsEnabled property"""
        return self.properties.get("isRelatedTenantsEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TenantGovernanceSetting"
