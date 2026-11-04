from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ItemActionStat(ClientValue):
    """The itemActionStat resource provides aggregate details about an action over a period of time."""

    actionCount: int | None = None
    actorCount: int | None = None
    accessCount: int | None = None
    viewCount: int | None = None
    shareCount: int | None = None
    downloadCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ItemActionStat"
