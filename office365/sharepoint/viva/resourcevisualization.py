from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ResourceVisualization(ClientValue):
    Acronym: str | None = None
    Color: str | None = None
    PreviewImageUrl: str | None = None
