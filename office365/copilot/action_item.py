from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ActionItem(ClientValue):
    ownerDisplayName: str | None = None
    text: str | None = None
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ActionItem"
