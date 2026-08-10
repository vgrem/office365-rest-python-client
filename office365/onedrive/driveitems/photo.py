from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class Photo(ClientValue):
    """The photo resource provides photo and camera properties, for example, EXIF metadata, on a driveItem."""

    cameraMake: str | None = None
    cameraModel: str | None = None
    exposureDenominator: float | None = None
    exposureNumerator: float | None = None
    fNumber: float | None = None
    focalLength: float | None = None
    iso: int | None = None
    orientation: int | None = None
    takenDateTime: datetime | None = field(default_factory=lambda: datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Photo"
