from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.filter import ConditionalAccessFilter
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ConditionalAccessApplications(ClientValue):
    applicationFilter: ConditionalAccessFilter = field(default_factory=ConditionalAccessFilter)
    excludeApplications: StringCollection = field(default_factory=StringCollection)
    includeApplications: StringCollection = field(default_factory=StringCollection)
    includeAuthenticationContextClassReferences: StringCollection = field(default_factory=StringCollection)
    includeUserActions: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessApplications"
