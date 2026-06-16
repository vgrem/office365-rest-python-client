from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class TileData(ClientValue):
    """Represents a Tile that describes a graphical link the user can click."""

    BackgroundCollageImageLocations: StringCollection | None = None
    IsWide: Optional[bool] = None
    LinkLocation: Optional[str] = None
    TileOrder: Optional[int] = None
    Title: Optional[str] = None
    TransparentOverlay: Optional[bool] = None
    BackgroundImageLocation: str | None = None
    BackgroundImageRendersAsIcon: bool | None = None
    BodyText: str | None = None
    Description: str | None = None
    HoverDisabled: bool | None = None
    ID: int | None = None

    @property
    def entity_type_name(self):
        return "SP.WebParts.TileData"
