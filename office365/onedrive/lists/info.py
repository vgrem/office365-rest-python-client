from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ListInfo(ClientValue):
    """
    The listInfo complex type provides additional information about a list.
    """

    template: str | None = None
    contentTypesEnabled: bool = False
    hidden: bool = False

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ListInfo"
