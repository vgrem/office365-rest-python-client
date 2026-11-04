from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class OutOfOfficeSettings(ClientValue):
    isOutOfOffice: bool | None = None
    message: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OutOfOfficeSettings"
