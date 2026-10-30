from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.relationship_creation_type import RelationshipCreationType
    from office365.directory.relationship_policy import RelationshipPolicy
    from office365.directory.relationship_status import RelationshipStatus


class GovernanceRelationship(Entity):
    @odata(name="createdType")
    @property
    def created_type(self) -> RelationshipCreationType:
        """Gets the createdType property"""
        from office365.directory.relationship_creation_type import (
            RelationshipCreationType,
        )

        return self.properties.get("createdType", RelationshipCreationType.approvedByAdmin)

    @odata(name="creationDateTime")
    @property
    def creation_date_time(self) -> Optional[datetime]:
        """Gets the creationDateTime property"""
        return self.properties.get("creationDateTime", datetime.min)

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

    @odata(name="policySnapshot")
    @property
    def policy_snapshot(self) -> RelationshipPolicy:
        """Gets the policySnapshot property"""
        from office365.directory.relationship_policy import RelationshipPolicy

        return self.properties.get("policySnapshot", RelationshipPolicy())

    @odata(name="status")
    @property
    def status(self) -> RelationshipStatus:
        """Gets the status property"""
        from office365.directory.relationship_status import RelationshipStatus

        return self.properties.get("status", RelationshipStatus.active)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GovernanceRelationship"
