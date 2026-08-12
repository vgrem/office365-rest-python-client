from __future__ import annotations

from dataclasses import dataclass

from office365.outlook.selectionlikelihoodinfo import SelectionLikelihoodInfo
from office365.runtime.client_value import ClientValue


@dataclass
class ScoredEmailAddress(ClientValue):
    address: str | None = None
    itemId: str | None = None
    relevanceScore: float | None = None
    selectionLikelihood: SelectionLikelihoodInfo = SelectionLikelihoodInfo.notSpecified

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ScoredEmailAddress"
