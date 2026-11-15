from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SchedulingGroupInfo(ClientValue):
    code: str | None = None
    displayName: str | None = None
    schedulingGroupId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SchedulingGroupInfo"
