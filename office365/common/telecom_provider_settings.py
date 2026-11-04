from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TelecomProviderSettings(ClientValue):
    appId: UUID | None = None
    isEvaluationModeEnabled: bool | None = None
    migrationPercentage: int | None = None
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TelecomProviderSettings"
