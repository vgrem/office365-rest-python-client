from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ResourceVisualization(ClientValue):
    Acronym: str | None = None
    Color: str | None = None
    PreviewImageUrl: str | None = None
