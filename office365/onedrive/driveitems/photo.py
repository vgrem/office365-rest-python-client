from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Photo(ClientValue):
    """The photo resource provides photo and camera properties, for example, EXIF metadata, on a driveItem."""

    cameraMake: str | None = None
    cameraModel: str | None = None
