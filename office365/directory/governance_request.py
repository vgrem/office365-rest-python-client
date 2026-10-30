from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.request_status import RequestStatus
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.relationship_policy import RelationshipPolicy
    from office365.directory.tenant_governance_policy_template import (
        TenantGovernancePolicyTemplate,
    )


class GovernanceRequest(Entity):
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

    @odata(name="policySnapshot")
    @property
    def policy_snapshot(self) -> RelationshipPolicy:
        """Gets the policySnapshot property"""
        from office365.directory.relationship_policy import RelationshipPolicy

        return self.properties.get("policySnapshot", RelationshipPolicy())

    @odata(name="requestDateTime")
    @property
    def request_date_time(self) -> Optional[datetime]:
        """Gets the requestDateTime property"""
        return self.properties.get("requestDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> RequestStatus:
        """Gets the status property"""
        return self.properties.get("status", RequestStatus.pending)

    @odata(name="governancePolicyTemplate", navigation=True)
    @property
    def governance_policy_template(self) -> TenantGovernancePolicyTemplate:
        """Gets the governancePolicyTemplate property"""
        from office365.directory.tenant_governance_policy_template import (
            TenantGovernancePolicyTemplate,
        )

        return self.properties.get(
            "governancePolicyTemplate",
            TenantGovernancePolicyTemplate(self.context, ResourcePath("governancePolicyTemplate", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GovernanceRequest"
