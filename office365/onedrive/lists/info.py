from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
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
