from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.search.alteration import SearchAlteration
from office365.search.alterationtype import SearchAlterationType


class AlterationResponse(ClientValue):
    originalQueryString: str | None = None
    queryAlteration: SearchAlteration = field(default_factory=SearchAlteration)
    queryAlterationType: SearchAlterationType = SearchAlterationType.suggestion

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AlterationResponse"
