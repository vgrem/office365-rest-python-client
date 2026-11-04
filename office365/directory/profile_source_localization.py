from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ProfileSourceLocalization(ClientValue):
    displayName: str | None = None
    languageTag: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProfileSourceLocalization"
