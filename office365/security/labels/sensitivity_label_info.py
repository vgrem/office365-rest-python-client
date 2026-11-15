from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SensitivityLabelInfo(ClientValue):
    color: str | None = None
    displayName: str | None = None
    priority: int | None = None
    sensitivityLabelId: str | None = None
    tooltip: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SensitivityLabelInfo"
