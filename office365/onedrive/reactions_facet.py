from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ReactionsFacet(ClientValue):
    commentCount: int | None = None
    likeCount: int | None = None
    shareCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ReactionsFacet"
