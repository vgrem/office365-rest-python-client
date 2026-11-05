from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ProfileSourceLocalization(ClientValue):
    displayName: str | None = None
    languageTag: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProfileSourceLocalization"
