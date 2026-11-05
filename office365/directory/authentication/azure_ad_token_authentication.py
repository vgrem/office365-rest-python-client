from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AzureAdTokenAuthentication(ClientValue):
    resourceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AzureAdTokenAuthentication"
