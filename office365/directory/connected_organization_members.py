from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ConnectedOrganizationMembers(ClientValue):
    connectedOrganizationId: str | None = None
    description: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConnectedOrganizationMembers"
