from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class VisualizationAppInfo(ClientValue):
    DesignUri: str | None = None
    Id: UUID | None = None
    RuntimeUri: str | None = None
