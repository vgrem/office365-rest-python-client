from __future__ import annotations

from typing import Optional

from office365.directory.tenantinformation.multitenantorganizationmemberrole import MultiTenantOrganizationMemberRole
from office365.directory.tenantinformation.multitenantorganizationmemberstate import MultiTenantOrganizationMemberState
from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.audit.multi_tenant_organization_join_request_transition_details import (  # noqa: E501
    MultiTenantOrganizationJoinRequestTransitionDetails,
)


class MultiTenantOrganizationJoinRequestRecord(Entity):
    @odata(name="addedByTenantId")
    @property
    def added_by_tenant_id(self) -> Optional[str]:
        """Gets the addedByTenantId property"""
        return self.properties.get("addedByTenantId", None)

    @odata(name="memberState")
    @property
    def member_state(self) -> MultiTenantOrganizationMemberState:
        """Gets the memberState property"""
        return self.properties.get("memberState", MultiTenantOrganizationMemberState.pending)

    @odata(name="role")
    @property
    def role(self) -> MultiTenantOrganizationMemberRole:
        """Gets the role property"""
        return self.properties.get("role", MultiTenantOrganizationMemberRole.owner)

    @odata(name="transitionDetails")
    @property
    def transition_details(self) -> MultiTenantOrganizationJoinRequestTransitionDetails:
        """Gets the transitionDetails property"""
        return self.properties.get("transitionDetails", MultiTenantOrganizationJoinRequestTransitionDetails())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantOrganizationJoinRequestRecord"
