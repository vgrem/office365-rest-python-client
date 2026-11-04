from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AppListItem(ClientValue):
    appId: str | None = None
    appStoreUrl: str | None = None
    name: str | None = None
    publisher: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppListItem"
