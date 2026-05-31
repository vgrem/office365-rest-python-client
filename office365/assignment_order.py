from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from dataclasses import dataclass, field

@dataclass
class AssignmentOrder(ClientValue):
    order: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AssignmentOrder'