from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.search.retrieval_hit import RetrievalHit


@value
class RetrievalResponse(ClientValue):
    retrievalHits: ClientValueCollection[RetrievalHit] = field(
        default_factory=lambda: ClientValueCollection(RetrievalHit)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RetrievalResponse"
