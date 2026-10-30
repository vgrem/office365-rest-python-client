from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.delegated_administration_role_assignment import DelegatedAdministrationRoleAssignment
from office365.directory.multi_tenant_applications_to_provision import MultiTenantApplicationsToProvision
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class TenantGovernancePolicyTemplate(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="delegatedAdministrationRoleAssignments")
    @property
    def delegated_administration_role_assignments(self) -> ClientValueCollection[DelegatedAdministrationRoleAssignment]:
        """Gets the delegatedAdministrationRoleAssignments property"""
        return self.properties.get(
            "delegatedAdministrationRoleAssignments",
            ClientValueCollection[DelegatedAdministrationRoleAssignment](DelegatedAdministrationRoleAssignment),
        )

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="governedTenantCanTerminate")
    @property
    def governed_tenant_can_terminate(self) -> Optional[bool]:
        """Gets the governedTenantCanTerminate property"""
        return self.properties.get("governedTenantCanTerminate", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="multiTenantApplicationsToProvision")
    @property
    def multi_tenant_applications_to_provision(self) -> ClientValueCollection[MultiTenantApplicationsToProvision]:
        """Gets the multiTenantApplicationsToProvision property"""
        return self.properties.get(
            "multiTenantApplicationsToProvision",
            ClientValueCollection[MultiTenantApplicationsToProvision](MultiTenantApplicationsToProvision),
        )

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TenantGovernancePolicyTemplate"
