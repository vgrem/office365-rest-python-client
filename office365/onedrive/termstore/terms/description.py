from __future__ import annotations

from office365.runtime.client_value import ClientValue


class LocalizedDescription(ClientValue):
    """Represents the localized description used to describe a term in the term store."""

    languageTag: str | None = None
    description: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.termStore.LocalizedDescription"
