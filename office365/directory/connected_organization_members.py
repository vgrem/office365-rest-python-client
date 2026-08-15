from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ConnectedOrganizationMembers(ClientValue):
    connectedOrganizationId: str | None = None
    description: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConnectedOrganizationMembers"
