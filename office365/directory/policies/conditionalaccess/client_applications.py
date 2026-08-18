from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.filter import ConditionalAccessFilter
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ConditionalAccessClientApplications(ClientValue):
    excludeServicePrincipals: StringCollection = field(default_factory=StringCollection)
    includeServicePrincipals: StringCollection = field(default_factory=StringCollection)
    servicePrincipalFilter: ConditionalAccessFilter = field(default_factory=ConditionalAccessFilter)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessClientApplications"
