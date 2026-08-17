from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AppConsentRequestScope(ClientValue):
    displayName: str | None = None
    "The appConsentRequestScope details the dynamic permission scopes for which access is being requested."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppConsentRequestScope"
