from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.query_type import QueryType


@value
class EventQuery(ClientValue):
    query: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EventQuery"

    queryType: QueryType = QueryType.files
