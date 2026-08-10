from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
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
