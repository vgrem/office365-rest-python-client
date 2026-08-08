from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.match_mode import MatchMode
from office365.directory.identitygovernance.quarantine_condition import QuarantineCondition
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class QuarantineConfiguration(ClientValue):
    conditions: ClientValueCollection[QuarantineCondition] = field(
        default_factory=lambda: ClientValueCollection(QuarantineCondition)
    )
    matchMode: MatchMode = MatchMode.any

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.QuarantineConfiguration"
