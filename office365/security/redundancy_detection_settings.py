from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class RedundancyDetectionSettings(ClientValue):
    isEnabled: bool | None = None
    maxWords: int | None = None
    minWords: int | None = None
    similarityThreshold: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RedundancyDetectionSettings"
