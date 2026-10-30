from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class GovernanceInvitation(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="governedTenantId")
    @property
    def governed_tenant_id(self) -> Optional[str]:
        """Gets the governedTenantId property"""
        return self.properties.get("governedTenantId", None)

    @odata(name="governedTenantName")
    @property
    def governed_tenant_name(self) -> Optional[str]:
        """Gets the governedTenantName property"""
        return self.properties.get("governedTenantName", None)

    @odata(name="governingTenantId")
    @property
    def governing_tenant_id(self) -> Optional[str]:
        """Gets the governingTenantId property"""
        return self.properties.get("governingTenantId", None)

    @odata(name="governingTenantName")
    @property
    def governing_tenant_name(self) -> Optional[str]:
        """Gets the governingTenantName property"""
        return self.properties.get("governingTenantName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GovernanceInvitation"
