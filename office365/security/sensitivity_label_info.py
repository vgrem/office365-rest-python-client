from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SensitivityLabelInfo(ClientValue):
    color: str | None = None
    displayName: str | None = None
    priority: int | None = None
    sensitivityLabelId: str | None = None
    tooltip: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SensitivityLabelInfo"
