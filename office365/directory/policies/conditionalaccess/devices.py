from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.filter import ConditionalAccessFilter
from office365.runtime.client_value import ClientValue


@dataclass
class ConditionalAccessDevices(ClientValue):
    deviceFilter: ConditionalAccessFilter = field(default_factory=ConditionalAccessFilter)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessDevices"
