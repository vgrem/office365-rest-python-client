from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class NavigationNodeCreationInformation(ClientValue):
    """
    Describes a new navigation node to be created.
    """

    Title: str | None = None
    Url: str | None = None
    IsExternal: bool = False
    AsLastNode: bool = False
    PreviousNode: NavigationNodeCreationInformation | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.NavigationNode"

    ExpectedParentContainerId: int | None = None
