from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.directory.tenantinformation.multitenantorganizationmemberrole import MultiTenantOrganizationMemberRole
from office365.directory.tenantinformation.multitenantorganizationmemberstate import MultiTenantOrganizationMemberState
from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.audit.multi_tenant_organization_member_transition_details import (  # noqa: E501
    MultiTenantOrganizationMemberTransitionDetails,
)


class MultiTenantOrganizationMember(Entity):
    @odata(name="addedByTenantId")
    @property
    def added_by_tenant_id(self) -> Optional[UUID]:
        """Gets the addedByTenantId property"""
        return self.properties.get("addedByTenantId", None)

    @odata(name="addedDateTime")
    @property
    def added_date_time(self) -> Optional[datetime]:
        """Gets the addedDateTime property"""
        return self.properties.get("addedDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="joinedDateTime")
    @property
    def joined_date_time(self) -> Optional[datetime]:
        """Gets the joinedDateTime property"""
        return self.properties.get("joinedDateTime", datetime.min)

    @odata(name="role")
    @property
    def role(self) -> MultiTenantOrganizationMemberRole:
        """Gets the role property"""
        return self.properties.get("role", MultiTenantOrganizationMemberRole.owner)

    @odata(name="state")
    @property
    def state(self) -> MultiTenantOrganizationMemberState:
        """Gets the state property"""
        return self.properties.get("state", MultiTenantOrganizationMemberState.pending)

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="transitionDetails")
    @property
    def transition_details(self) -> MultiTenantOrganizationMemberTransitionDetails:
        """Gets the transitionDetails property"""
        return self.properties.get("transitionDetails", MultiTenantOrganizationMemberTransitionDetails())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MultiTenantOrganizationMember"
