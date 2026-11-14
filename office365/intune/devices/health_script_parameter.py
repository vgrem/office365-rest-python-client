from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DeviceHealthScriptParameter(ClientValue):
    applyDefaultValueWhenNotAssigned: bool | None = None
    description: str | None = None
    isRequired: bool | None = None
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceHealthScriptParameter"
