from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class TileData(ClientValue):

    """Represents a Tile that describes a graphical link the user can click."""

    BackgroundCollageImageLocations: StringCollection | None = None
    BackgroundImageLocation = None
    BackgroundImageRendersAsIcon = None
    BodyText = None
    Description = None
    HoverDisabled = None
    ID = None
    IsWide: Optional[bool] = None
    LinkLocation: Optional[str] = None
    TileOrder: Optional[int] = None
    Title: Optional[str] = None
    TransparentOverlay: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.WebParts.TileData"