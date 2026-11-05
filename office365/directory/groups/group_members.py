from __future__ import annotations

from office365.runtime.client_value import ClientValue


class GroupMembers(ClientValue):
    description: str | None = None
    groupId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupMembers"
