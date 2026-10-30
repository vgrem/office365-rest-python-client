from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.multi_tenant_organization_identity_sync_policy_template import (
        MultiTenantOrganizationIdentitySyncPolicyTemplate,
    )
    from office365.directory.multi_tenant_organization_partner_configuration_template import (
        MultiTenantOrganizationPartnerConfigurationTemplate,
    )


class PolicyTemplate(Entity):
    """Represents the base policy in the directory for multitenant organization settings."""

    @odata(name="multiTenantOrganizationIdentitySynchronization", navigation=True)
    @property
    def multi_tenant_organization_identity_synchronization(self) -> MultiTenantOrganizationIdentitySyncPolicyTemplate:
        """Gets the multiTenantOrganizationIdentitySynchronization property"""
        from office365.directory.multi_tenant_organization_identity_sync_policy_template import (
            MultiTenantOrganizationIdentitySyncPolicyTemplate,
        )

        return self.properties.get(
            "multiTenantOrganizationIdentitySynchronization",
            MultiTenantOrganizationIdentitySyncPolicyTemplate(
                self.context, ResourcePath("multiTenantOrganizationIdentitySynchronization", self.resource_path)
            ),
        )

    @odata(name="multiTenantOrganizationPartnerConfiguration", navigation=True)
    @property
    def multi_tenant_organization_partner_configuration(self) -> MultiTenantOrganizationPartnerConfigurationTemplate:
        """Gets the multiTenantOrganizationPartnerConfiguration property"""
        from office365.directory.multi_tenant_organization_partner_configuration_template import (
            MultiTenantOrganizationPartnerConfigurationTemplate,
        )

        return self.properties.get(
            "multiTenantOrganizationPartnerConfiguration",
            MultiTenantOrganizationPartnerConfigurationTemplate(
                self.context, ResourcePath("multiTenantOrganizationPartnerConfiguration", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyTemplate"
