from __future__ import annotations

from office365.directory.policies.conditionalaccess.externaltenantsmembershipkind import (
    ConditionalAccessExternalTenantsMembershipKind,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ConditionalAccessExternalTenants(ClientValue):
    membershipKind: ConditionalAccessExternalTenantsMembershipKind = ConditionalAccessExternalTenantsMembershipKind.all

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessExternalTenants"
