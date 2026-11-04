from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ClassificationInnerError(ClientValue):
    activityId: str | None = None
    clientRequestId: str | None = None
    code: str | None = None
    errorDateTime: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ClassificationInnerError"
