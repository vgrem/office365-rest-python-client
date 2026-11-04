from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DisplayNameLocalization(ClientValue):
    """Provides the ability for an administrator to customize the string used in a shared Microsoft 365 experience."""

    displayName: str | None = None
    languageTag: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DisplayNameLocalization"
