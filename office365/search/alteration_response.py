from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.search.alterationtype import SearchAlterationType
from office365.search.search_alteration import SearchAlteration


@value
class AlterationResponse(ClientValue):
    originalQueryString: str | None = None
    queryAlteration: SearchAlteration = field(default_factory=SearchAlteration)
    queryAlterationType: SearchAlterationType = SearchAlterationType.suggestion

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AlterationResponse"
