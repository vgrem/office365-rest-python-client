from __future__ import annotations

from dataclasses import field

from office365.directory.policies.conditionalaccess.external_tenants import ConditionalAccessExternalTenants
from office365.runtime.types.collections import StringCollection


class ConditionalAccessEnumeratedExternalTenants(ConditionalAccessExternalTenants):
    members: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessEnumeratedExternalTenants"
