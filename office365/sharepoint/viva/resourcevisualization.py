from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ResourceVisualization(ClientValue):
    Acronym: str | None = None
    Color: str | None = None
    PreviewImageUrl: str | None = None
